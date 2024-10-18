"""
Simple Lattice Mirror

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

from .preferences import register_preferences, unregister_preferences
from .panel import register_panel, unregister_panel
from .handler import register_handlers, unregister_handlers


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


def register():
    """
    register each module
    """
    register_panel()
    register_handlers()
    register_preferences()


def unregister():
    """
    unregister each module
    """
    unregister_panel()
    unregister_handlers()
    unregister_preferences()


if __name__ == "__main__":
    register()
