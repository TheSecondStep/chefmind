"""
中间件
"""

from langchain.agents.middleware import AgentMiddleware
from langchain_core.messages import ToolMessage


class CustomToolErrorMiddleware(AgentMiddleware):
    """
    自定义工具调用异常中间件
    """

    async def awrap_tool_call(self, request, handler):
        """ Intercept and control async model execution. """
        try:
            return await handler(request)
        except Exception as e:
            return ToolMessage(
                content=f"\r\nCustomToolErrorMiddleware：工具调用异常：{str(e)}\r\n",
                tool_call_id=request.tool_call["id"]
            )
