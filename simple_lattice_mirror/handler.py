import bpy
from .main import check_vertex_movement


def register_handlers():
    if check_vertex_movement not in bpy.app.handlers.depsgraph_update_post:
        bpy.app.handlers.depsgraph_update_post.append(check_vertex_movement)


def load_post_handler(_):
    register_handlers()
