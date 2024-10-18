import bpy
from .main import check_vertex_movement


def register_handlers():
    if check_vertex_movement not in bpy.app.handlers.depsgraph_update_post:
        bpy.app.handlers.depsgraph_update_post.append(check_vertex_movement)
    if load_post_handler not in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.append(load_post_handler)


def load_post_handler(_):
    register_handlers()


def unregister_handlers():
    if check_vertex_movement in bpy.app.handlers.depsgraph_update_post:
        bpy.app.handlers.depsgraph_update_post.remove(check_vertex_movement)
    if load_post_handler in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.remove(load_post_handler)
