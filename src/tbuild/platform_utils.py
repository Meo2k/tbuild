import platform

def get_current_os() -> str:
    """Detect current operating system key (linux, windows, darwin)."""
    sys_name = platform.system().lower()
    if sys_name == "linux":
        return "linux"
    elif sys_name == "windows":
        return "windows"
    elif sys_name in ("darwin", "macos"):
        return "darwin"
    return sys_name
