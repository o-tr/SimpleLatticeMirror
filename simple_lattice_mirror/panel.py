import bpy
from .handler import register_handlers
from .preferences import get_axis_key, get_toggle_key


def is_active_object_lattice(context) -> bool:
    return context.active_object and context.active_object.type == "LATTICE"


class SimpleLatticeMirrorPanel(bpy.types.Panel):
    bl_label = "SimpleLatticeMirror"
    bl_idname = "OBJECT_PT_simple_lattice_mirror"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Item"

    @classmethod
    def poll(self, context) -> bool:
        return is_active_object_lattice(context)

    def draw(self, context) -> None:
        layout = self.layout
        layout.prop(context.scene, get_axis_key(), text="Axis", expand=True)
        layout.prop(context.scene, get_toggle_key(), text="Toggle", expand=True)
        register_handlers()


def register_panel():
    bpy.utils.register_class(SimpleLatticeMirrorPanel)


def unregister_panel():
    if SimpleLatticeMirrorPanel in bpy.types.Panel:
        bpy.utils.unregister_class(SimpleLatticeMirrorPanel)
