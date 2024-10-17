import bpy


class SimpleLatticeMirrorPanel(bpy.types.Panel):
    bl_label = "SimpleLatticeMirror"
    bl_idname = "jp.ootr.simple_lattice_mirror.panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Item"

    @classmethod
    def poll(self, context) -> bool:
        return context.active_object and context.active_object.type == "LATTICE"

    def draw(self, context) -> None:
        layout = self.layout
        layout.prop(
            context.scene, "simple_lattice_mirror_axis", text="Axis", expand=True
        )
        layout.prop(
            context.scene, "simple_lattice_mirror_toggle", text="Toggle", expand=True
        )
        register_handlers()
