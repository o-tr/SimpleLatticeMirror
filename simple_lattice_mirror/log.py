from .preferences import is_debug_enabled


def log(message) -> None:
    """
    Print a message to the console if debug mode is enabled
    """
    if not is_debug_enabled():
        return
    print(f"{__package__}: {message}")
