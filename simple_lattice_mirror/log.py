import bpy

def log(message) -> None:
    if not bpy.context.preferences.addons[__name__].preferences.debug:
        return
    print(f"SimpleLatticeMirror: {message}")
