import bpy
from .handler import register_handlers
from .preferences import get_axis_key, get_toggle_key


def is_active_object_lattice(context) -> bool:
    """
    Check if the active object is a lattice
    """
    return context.active_object and context.active_object.type == "LATTICE"


class SimpleLatticeMirrorPanel(bpy.types.Panel):
    """
    Simple Lattice Mirror Panel
    """

    bl_label = "SimpleLatticeMirror"
    bl_idname = "OBJECT_PT_simple_lattice_mirror"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Item"

    @classmethod
    def poll(cls, context) -> bool:
        """
        show the panel only if the active object is a lattice
        """
        return is_active_object_lattice(context)

    def draw(self, context) -> None:
        """
        Draw the panel
        """
        layout = self.layout
        layout.prop(context.scene, get_axis_key(), text="Axis", expand=True)
        layout.prop(context.scene, get_toggle_key(), text="Toggle", expand=True)
        register_handlers()


def register_panel():
    """
    Register the panel
    """
    bpy.utils.register_class(SimpleLatticeMirrorPanel)


def unregister_panel():
    """
    Unregister the panel
    """
    bpy.utils.unregister_class(SimpleLatticeMirrorPanel)
