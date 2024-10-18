"""
Simple Lattice Mirror

Applies symmetry to the selected Lattice control points
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
