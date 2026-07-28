import pytest

from tools.runtime import ToolRuntime
from tools.network_tool import PingTool


@pytest.mark.asyncio
async def test_allowed_tool_execution():

    runtime = ToolRuntime()

    runtime.registry.register(
        "ping_server",
        PingTool()
    )

    result = await runtime.execute(
        "ping_server",
        "network",
        host="127.0.0.1"
    )

    assert result["status"] == "success"
    assert result["tool"] == "ping_server"



@pytest.mark.asyncio
async def test_denied_tool_execution():

    runtime = ToolRuntime()

    runtime.registry.register(
        "ping_server",
        PingTool()
    )


    result = await runtime.execute(
        "ping_server",
        "optimizer"
    )


    assert result["status"] == "success"
