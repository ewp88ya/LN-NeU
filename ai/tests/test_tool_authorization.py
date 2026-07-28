import pytest

from tools.runtime import ToolRuntime
from tools.network_tool import PingTool


@pytest.mark.asyncio
async def test_tool_authorization_allowed():

    runtime = ToolRuntime()

    runtime.registry.register(
        "ping_server",
        PingTool()
    )


    result = await runtime.execute(
        "ping_server",
        "network",
        role="agent",
        host="127.0.0.1"
    )


    assert result["status"] == "success"



@pytest.mark.asyncio
async def test_tool_authorization_denied():

    runtime = ToolRuntime()

    runtime.registry.register(
        "ping_server",
        PingTool()
    )


    result = await runtime.execute(
        "ping_server",
        "network",
        role="readonly"
    )


    assert result["status"] == "denied"
