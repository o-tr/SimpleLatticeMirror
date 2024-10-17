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


def register_preferences() -> None:
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


def unregister_preferences() -> None:
    bpy.utils.unregister_class(SimpleLatticeMirrorPreferences)
    del bpy.types.Scene.simple_lattice_mirror_axis
    del bpy.types.Scene.simple_lattice_mirror_toggle


def get_threshold() -> float:
    return bpy.context.preferences.addons[__package__].preferences.threshold


def is_debug_enabled() -> bool:
    return bpy.context.preferences.addons[__package__].preferences.debug


def get_axis() -> str:
    return bpy.context.scene.simple_lattice_mirror_axis


def get_toggle() -> bool:
    return bpy.context.scene.simple_lattice_mirror_toggle == "ON"
