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
    "version": (0, 0, 4),
    "blender": (3, 0, 0),
    "location": "View3D > Tool Shelf > Item",
    "description": "Applies symmetry to the selected Lattice control points",
    "category": "Object",
    "license": "MIT",
}

import bpy

from .main import check_vertex_movement
from .SimpleLatticeMirrorPanel import SimpleLatticeMirrorPanel
from .SimpleLatticeMirrorPreferences import SimpleLatticeMirrorPreferences

name = __name__


def register():
    bpy.utils.register_class(SimpleLatticeMirrorPanel)
    bpy.utils.register_class(SimpleLatticeMirrorPreferences)

    bpy.types.Scene.simple_lattice_mirror_axis = bpy.props.EnumProperty(
        name="Axis",
        description="Axis to mirror mirror on",
        items=[
            ("X", "X", "Mirror on the X axis"),
            ("Y", "Y", "Mirror on the Y axis"),
            ("Z", "Z", "Mirror on the Z axis"),
        ],
        default="X",
    )

    bpy.types.Scene.simple_lattice_mirror_toggle = bpy.props.EnumProperty(
        name="Toggle",
        description="Toggle mirror",
        items=[("OFF", "OFF", "Toggle mirror OFF"), ("ON", "ON", "Toggle mirror ON")],
        default="OFF",
    )

    bpy.app.handlers.depsgraph_update_post.append(check_vertex_movement)


def unregister():
    bpy.utils.unregister_class(SimpleLatticeMirrorPanel)
    bpy.utils.unregister_class(SimpleLatticeMirrorPreferences)

    bpy.app.handlers.depsgraph_update_post.remove(check_vertex_movement)

    del bpy.types.Scene.simple_lattice_mirror_axis
    del bpy.types.Scene.simple_lattice_mirror_toggle


if __name__ == "__main__":
    register()
