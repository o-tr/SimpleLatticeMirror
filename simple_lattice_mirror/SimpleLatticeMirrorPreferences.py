import bpy

from . import name

class SimpleLatticeMirrorPreferences(bpy.types.AddonPreferences):
    bl_idname = name

    threshold: bpy.props.FloatProperty(
        name="Threshold",
        description="Threshold for identifying symmetric points",
        default=0.001
    )

    debug: bpy.props.BoolProperty(
        name="Debug",
        description="Enable debug logging",
        default=False
    )

    def draw(self, _) -> None:
        layout = self.layout
        layout.prop(self, "debug")
        layout.prop(self, "threshold")