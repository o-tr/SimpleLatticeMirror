import bpy

from . import name


def log(message) -> None:
    if not bpy.context.preferences.addons[name].preferences.debug:
        return
    print(f"SimpleLatticeMirror: {message}")
