class LNNeUError(Exception):
    """
    Base exception LN-NeU
    """
    pass



class TaskExecutionError(LNNeUError):
    """
    Task gagal dieksekusi
    """
    pass



class AgentExecutionError(LNNeUError):
    """
    Agent gagal menjalankan proses
    """
    pass



class ToolExecutionError(LNNeUError):
    """
    Tool gagal digunakan
    """
    pass
