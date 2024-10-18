import bpy
from .main import tick


def register_handlers():
    """
    Register the handlers
    """
    if tick not in bpy.app.handlers.depsgraph_update_post:
        bpy.app.handlers.depsgraph_update_post.append(tick)
    if load_post_handler not in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.append(load_post_handler)


def load_post_handler(_):
    """
    Register the handlers on load
    """
    register_handlers()


def unregister_handlers():
    """
    Unregister the handlers
    """
    if tick in bpy.app.handlers.depsgraph_update_post:
        bpy.app.handlers.depsgraph_update_post.remove(tick)
    if load_post_handler in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.remove(load_post_handler)
