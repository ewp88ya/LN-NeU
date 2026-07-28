from tools.permission import ToolPermission


def test_network_tool_permission():

    permission = ToolPermission()

    assert permission.allowed(
        "network",
        "ping_server"
    )

    assert permission.allowed(
        "network",
        "dns_lookup"
    )



def test_optimizer_restricted_permission():

    permission = ToolPermission()

    assert permission.allowed(
        "optimizer",
        "ping_server"
    )


    assert not permission.allowed(
        "optimizer",
        "dns_lookup"
    )



def test_unknown_tool_denied():

    permission = ToolPermission()


    assert not permission.allowed(
        "network",
        "unknown_tool"
    )
