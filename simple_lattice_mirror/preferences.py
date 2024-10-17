import bpy


class SimpleLatticeMirrorPreferences(bpy.types.AddonPreferences):
    """
    Preferences for the Simple Lattice Mirror add-on.
    """

    bl_idname = __package__

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


def get_threshold() -> float:
    return bpy.context.preferences.addons[__package__].preferences.threshold


def is_debug_enabled() -> bool:
    return bpy.context.preferences.addons[__package__].preferences.debug
