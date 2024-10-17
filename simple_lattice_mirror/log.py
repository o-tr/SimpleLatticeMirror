import bpy


def log(message) -> None:
    if not bpy.context.preferences.addons[__package__].preferences.debug:
        return
    print(f"{__package__}: {message}")
