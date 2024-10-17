import bpy


class SimpleLatticeMirrorPreferences(bpy.types.AddonPreferences):
    """
    Preferences for the Simple Lattice Mirror add-on.
    """

    bl_idname = "jp.ootr.simple_lattice_mirror.preferences"

    threshold: bpy.props.FloatProperty(
        name="Threshold",
        description="Threshold for identifying symmetric points",
        default=0.001,
    )

    debug: bpy.props.BoolProperty(
        name="Debug", description="Enable debug logging", default=False
    )

    def draw(self, _) -> None:
        layout = self.layout
        layout.prop(self, "debug")
        layout.prop(self, "threshold")
