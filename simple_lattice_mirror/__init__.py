"""
MIT License

Copyright (c) 2024 ootr

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

bl_info = {
    "name": "Simple Lattice Mirror",
    "author": "ootr",
    "version": (0, 0, 6),
    "blender": (3, 0, 0),
    "location": "View3D > Tool Shelf > Item",
    "description": "Applies symmetry to the selected Lattice control points",
    "category": "Object",
    "license": "MIT",
}

import bpy

from .preferences import register_preferences, unregister_preferences
from .panel import SimpleLatticeMirrorPanel
from .main import check_vertex_movement
from .handler import register_handlers, load_post_handler


def register():
    bpy.utils.register_class(SimpleLatticeMirrorPanel)
    register_handlers()
    bpy.app.handlers.load_post.append(load_post_handler)
    register_preferences()


def unregister():
    bpy.utils.unregister_class(SimpleLatticeMirrorPanel)

    bpy.app.handlers.load_post.remove(load_post_handler)
    bpy.app.handlers.depsgraph_update_post.remove(check_vertex_movement)
    unregister_preferences()


if __name__ == "__main__":
    register()
