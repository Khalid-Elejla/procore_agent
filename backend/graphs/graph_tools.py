from __future__ import annotations
from langgraph.prebuilt import ToolNode

from copy import copy

from langchain_core.runnables import RunnableConfig

from langchain_core.runnables.utils import Input


from langgraph.store.base import BaseStore

import asyncio

from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    List,
    Literal,
    Optional,
    Sequence,
    Tuple,
    Type,
    Union,
    cast,
)

from langchain_core.messages import (
    AIMessage,
    AnyMessage,
    ToolCall,
    ToolMessage,
)
from langchain_core.runnables import RunnableConfig
from langchain_core.runnables.config import (
    get_config_list,
    get_executor_for_config,
)
from langchain_core.runnables.utils import Input
from langchain_core.tools import BaseTool, InjectedToolArg
from langchain_core.tools import tool as create_tool
from typing_extensions import Annotated, get_args, get_origin

from langgraph.store.base import BaseStore
from langgraph.utils.runnable import RunnableCallable

from pydantic import BaseModel



def custom_tools_condition(
    state: Union[list[AnyMessage], dict[str, Any], BaseModel],
) -> Literal["tools", "__end__"]:
    
    if isinstance(state, list):
        ai_message = state[-1]
    elif isinstance(state, dict) and (messages := state.get("sql_agent_messages", [])):
        ai_message = messages[-1]
    elif messages := getattr(state, "sql_agent_messages", []):
        ai_message = messages[-1]
    else:
        raise ValueError(f"No messages found in input state to tool_edge: {state}")
    if hasattr(ai_message, "tool_calls") and len(ai_message.tool_calls) > 0:
        return "tools"
    return "__end__"


class SQLToolNode(ToolNode):  
    """Specialized ToolNode for SQL operations"""  

    def _parse_input(  
        self,  
        input: Union[  
            list[AnyMessage],  
            dict[str, Any],  
            BaseModel,  
        ],  
        store: BaseStore,  
    ) -> Tuple[List[ToolCall], Literal["list", "dict"]]:  
        if isinstance(input, list):  
            output_type = "list"  
            message = input[-1]  
        elif isinstance(input, dict):  
            output_type = "dict"  
            # Check sql_agent_messages first  
            messages = input.get("sql_agent_messages", []) or input.get("messages", [])  
            message = messages[-1] if messages else None  
        elif messages := getattr(input, "messages", None):  
            output_type = "dict"  
            message = messages[-1]  
        else:  
            raise ValueError("No message found in input")  

        if not isinstance(message, AIMessage):  
            raise ValueError("Last message is not an AIMessage")  

        tool_calls = [  
            self._inject_tool_args(call, input, store) for call in message.tool_calls  
        ]  
        return tool_calls, output_type  

    def _func(self, input: Union[list[AnyMessage], dict[str, Any], BaseModel],  
              config: RunnableConfig,  
              *,  
              store: BaseStore,  
    ) -> Any:  
        outputs = super()._func(input, config, store=store)  
        # Modify the output to use sql_agent_messages instead of messages  
        if isinstance(outputs, dict) and "messages" in outputs:  
            return {"sql_agent_messages": outputs["messages"]}  
        return outputs  
    

class AToolNode(RunnableCallable):
    """A node that runs the tools called in the last AIMessage.

    It can be used either in StateGraph with a "messages" key or in MessageGraph. If
    multiple tool calls are requested, they will be run in parallel. The output will be
    a list of ToolMessages, one for each tool call.

    The `ToolNode` is roughly analogous to:

    ```python
    tools_by_name = {tool.name: tool for tool in tools}
    def tool_node(state: dict):
        result = []
        for tool_call in state["messages"][-1].tool_calls:
            tool = tools_by_name[tool_call["name"]]
            observation = tool.invoke(tool_call["args"])
            result.append(ToolMessage(content=observation, tool_call_id=tool_call["id"]))
        return {"messages": result}
    ```

    Important:
        - The state MUST contain a list of messages.
        - The last message MUST be an `AIMessage`.
        - The `AIMessage` MUST have `tool_calls` populated.
    """

    name: str = "ToolNode"

    def __init__(
        self,
        tools: Sequence[Union[BaseTool, Callable]],
        *,
        name: str = "tools",
        tags: Optional[list[str]] = None,
        handle_tool_errors: Optional[bool] = True,
    ) -> None:
        super().__init__(self._func, self._afunc, name=name, tags=tags, trace=False)
        self.tools_by_name: Dict[str, BaseTool] = {}
        self.tool_to_state_args: Dict[str, Dict[str, Optional[str]]] = {}
        self.tool_to_store_arg: Dict[str, Optional[str]] = {}
        self.handle_tool_errors = handle_tool_errors
        for tool_ in tools:
            if not isinstance(tool_, BaseTool):
                tool_ = cast(BaseTool, create_tool(tool_))
            self.tools_by_name[tool_.name] = tool_
            self.tool_to_state_args[tool_.name] = _get_state_args(tool_)
            self.tool_to_store_arg[tool_.name] = _get_store_arg(tool_)

    def _func(
        self,
        input: Union[
            list[AnyMessage],
            dict[str, Any],
            BaseModel,
        ],
        config: RunnableConfig,
        *,
        store: BaseStore,
    ) -> Any:
        tool_calls, output_type = self._parse_input(input, store)
        config_list = get_config_list(config, len(tool_calls))
        with get_executor_for_config(config) as executor:
            outputs = [*executor.map(self._run_one, tool_calls, config_list)]
        # TypedDict, pydantic, dataclass, etc. should all be able to load from dict
        # return outputs if output_type == "list" else {"messages": outputs}
        return outputs if output_type == "list" else {"sql_agent_messages": outputs}
    

    def invoke(
        self, input: Input, config: Optional[RunnableConfig] = None, **kwargs: Any
    ) -> Any:
        if "store" not in kwargs:
            kwargs["store"] = None
        return super().invoke(input, config, **kwargs)

    async def ainvoke(
        self, input: Input, config: Optional[RunnableConfig] = None, **kwargs: Any
    ) -> Any:
        if "store" not in kwargs:
            kwargs["store"] = None
        return await super().ainvoke(input, config, **kwargs)

    async def _afunc(
        self,
        input: Union[
            list[AnyMessage],
            dict[str, Any],
            BaseModel,
        ],
        config: RunnableConfig,
        *,
        store: BaseStore,
    ) -> Any:
        tool_calls, output_type = self._parse_input(input, store)
        outputs = await asyncio.gather(
            *(self._arun_one(call, config) for call in tool_calls)
        )
        # TypedDict, pydantic, dataclass, etc. should all be able to load from dict
        # return outputs if output_type == "list" else {"messages": outputs}
        return outputs if output_type == "list" else {"sql_agent_messages": outputs}


    def _run_one(self, call: ToolCall, config: RunnableConfig) -> ToolMessage:
        if invalid_tool_message := self._validate_tool_call(call):
            return invalid_tool_message

        try:
            input = {**call, **{"type": "tool_call"}}
            tool_message: ToolMessage = self.tools_by_name[call["name"]].invoke(
                input, config
            )
            tool_message.content = cast(
                Union[str, list], msg_content_output(tool_message.content)
            )
            return tool_message
        except Exception as e:
            if not self.handle_tool_errors:
                raise e
            content = TOOL_CALL_ERROR_TEMPLATE.format(error=repr(e))
            return ToolMessage(content, name=call["name"], tool_call_id=call["id"])

    async def _arun_one(self, call: ToolCall, config: RunnableConfig) -> ToolMessage:
        if invalid_tool_message := self._validate_tool_call(call):
            return invalid_tool_message
        try:
            input = {**call, **{"type": "tool_call"}}
            tool_message: ToolMessage = await self.tools_by_name[call["name"]].ainvoke(
                input, config
            )
            tool_message.content = cast(
                Union[str, list], msg_content_output(tool_message.content)
            )
            return tool_message
        except Exception as e:
            if not self.handle_tool_errors:
                raise e
            content = TOOL_CALL_ERROR_TEMPLATE.format(error=repr(e))
            return ToolMessage(content, name=call["name"], tool_call_id=call["id"])

    def _parse_input(
        self,
        input: Union[
            list[AnyMessage],
            dict[str, Any],
            BaseModel,
        ],
        store: BaseStore,
    ) -> Tuple[List[ToolCall], Literal["list", "dict"]]:
        if isinstance(input, list):
            output_type = "list"
            message: AnyMessage = input[-1]
        # elif isinstance(input, dict) and (messages := input.get("messages", [])):
        elif isinstance(input, dict) and (messages := input.get("sql_agent_messages", [])):
            output_type = "dict"
            message = messages[-1]
#        elif messages := getattr(input, "messages", None):
        elif messages := getattr(input, "sql_agent_messages", None):

            # Assume dataclass-like state that can coerce from dict
            output_type = "dict"
            message = messages[-1]
        else:
            raise ValueError("No message found in input")

        if not isinstance(message, AIMessage):
            raise ValueError("Last message is not an AIMessage")

        tool_calls = [
            self._inject_tool_args(call, input, store) for call in message.tool_calls
        ]
        return tool_calls, output_type

    def _validate_tool_call(self, call: ToolCall) -> Optional[ToolMessage]:
        if (requested_tool := call["name"]) not in self.tools_by_name:
            content = INVALID_TOOL_NAME_ERROR_TEMPLATE.format(
                requested_tool=requested_tool,
                available_tools=", ".join(self.tools_by_name.keys()),
            )
            return ToolMessage(content, name=requested_tool, tool_call_id=call["id"])
        else:
            return None

    def _inject_state(
        self,
        tool_call: ToolCall,
        input: Union[
            list[AnyMessage],
            dict[str, Any],
            BaseModel,
        ],
    ) -> ToolCall:
        state_args = self.tool_to_state_args[tool_call["name"]]
        if state_args and isinstance(input, list):
            required_fields = list(state_args.values())
            if (
                len(required_fields) == 1
#                and required_fields[0] == "messages"
                and required_fields[0] == "sql_agent_messages"
                or required_fields[0] is None
            ):
#                input = {"messages": input}
                input = {"sql_agent_messages": input}

            else:
                err_msg = (
                    f"Invalid input to ToolNode. Tool {tool_call['name']} requires "
                    f"graph state dict as input."
                )
                if any(state_field for state_field in state_args.values()):
                    required_fields_str = ", ".join(f for f in required_fields if f)
                    err_msg += f" State should contain fields {required_fields_str}."
                raise ValueError(err_msg)
        if isinstance(input, dict):
            tool_state_args = {
                tool_arg: input[state_field] if state_field else input
                for tool_arg, state_field in state_args.items()
            }

        else:
            tool_state_args = {
                tool_arg: getattr(input, state_field) if state_field else input
                for tool_arg, state_field in state_args.items()
            }

        tool_call["args"] = {
            **tool_call["args"],
            **tool_state_args,
        }
        return tool_call

    def _inject_store(self, tool_call: ToolCall, store: BaseStore) -> ToolCall:
        store_arg = self.tool_to_store_arg[tool_call["name"]]
        if not store_arg:
            return tool_call

        if store is None:
            raise ValueError(
                "Cannot inject store into tools with InjectedStore annotations - "
                "please compile your graph with a store."
            )

        tool_call["args"] = {
            **tool_call["args"],
            store_arg: store,
        }
        return tool_call

    def _inject_tool_args(
        self,
        tool_call: ToolCall,
        input: Union[
            list[AnyMessage],
            dict[str, Any],
            BaseModel,
        ],
        store: BaseStore,
    ) -> ToolCall:
        if tool_call["name"] not in self.tools_by_name:
            return tool_call

        tool_call_copy: ToolCall = copy(tool_call)
        tool_call_with_state = self._inject_state(tool_call_copy, input)
        tool_call_with_store = self._inject_store(tool_call_with_state, store)
        return tool_call_with_store
