from .preferences import is_debug_enabled


def log(message) -> None:
    if not is_debug_enabled():
        return
    print(f"{__package__}: {message}")
