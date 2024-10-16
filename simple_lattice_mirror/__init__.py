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
    "version": (0, 0, 5),
    "blender": (3, 0, 0),
    "location": "View3D > Tool Shelf > Item",
    "description": "Applies symmetry to the selected Lattice control points",
    "category": "Object",
    "license": "MIT",
}

import bpy, math


class SimpleLatticeMirrorPreferences(bpy.types.AddonPreferences):
    """
    Preferences for the Simple Lattice Mirror add-on.
    """

    bl_idname = __name__

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


class SimpleLatticeMirrorPanel(bpy.types.Panel):
    bl_label = "SimpleLatticeMirror"
    bl_idname = "OBJECT_PT_SimpleLatticeMirror"
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


def log(message) -> None:
    if not bpy.context.preferences.addons[__name__].preferences.debug:
        return
    print(f"SimpleLatticeMirror: {message}")


def is_lattice_mirror_enabled() -> bool:
    return bpy.context.scene.simple_lattice_mirror_toggle == "ON"


def is_lattice_object(obj) -> bool:
    return obj and obj.type == "LATTICE"


def get_lattice_points(
    lattice: bpy.types.Lattice,
) -> tuple[list[int], list[list[float]]]:
    selected_point_indexes = [i for i, p in enumerate(lattice.points) if p.select]
    points = [[i[0], i[1], i[2]] for i in [p.co_deform.copy() for p in lattice.points]]
    return (selected_point_indexes, points)


def is_scene_updated(
    scene, points: list[list[float]], selected_points: list[int]
) -> bool:
    return (
        (not hasattr(check_vertex_movement, "previous_positions"))
        or (not hasattr(check_vertex_movement, "previous_selections"))
        or (not hasattr(check_vertex_movement, "symmetric_map"))
        or len(check_vertex_movement.previous_positions) != len(points)
        or check_vertex_movement.previous_selections != selected_points
        or check_vertex_movement.axis != scene.simple_lattice_mirror_axis
    )


def apply_symmetry(
    scene,
    lattice: bpy.types.Lattice,
    selected_point_indexes: list[int],
    points: list[list[float]],
) -> None:
    log(f"Selected point indexes: {selected_point_indexes}")
    for i, pointIndex in enumerate(selected_point_indexes):
        if points[pointIndex] == check_vertex_movement.previous_selections[i]:
            continue
        log(
            f"Vertex {pointIndex} has moved from {check_vertex_movement.previous_positions[pointIndex]} to {points[pointIndex]}"
        )
        log(f"Symmetric map: {check_vertex_movement.symmetric_map[i]}")
        for symmetric_index in check_vertex_movement.symmetric_map[i]:
            target_symmetric_point = convert_to_symmetric_point(
                points[pointIndex], scene.simple_lattice_mirror_axis
            )
            target_deform = lattice.points[symmetric_index].co_deform
            target_deform[0] = target_symmetric_point[0]
            target_deform[1] = target_symmetric_point[1]
            target_deform[2] = target_symmetric_point[2]
            points[symmetric_index] = target_symmetric_point
            log(f"Update point {symmetric_index} to {target_deform}")


def check_vertex_movement(scene) -> None:
    obj = bpy.context.active_object
    if not is_lattice_mirror_enabled() or not is_lattice_object(obj):
        return
    lattice: bpy.types.Lattice = obj.data
    (selected_point_indexes, points) = get_lattice_points(lattice)

    if is_scene_updated(scene, points, selected_point_indexes):
        log("Initialize previous_positions")
        check_vertex_movement.previous_positions = points
        check_vertex_movement.previous_selections = selected_point_indexes
        check_vertex_movement.axis = scene.simple_lattice_mirror_axis
        check_vertex_movement.symmetric_map = find_symmetric_point(
            lattice, scene.simple_lattice_mirror_axis
        )

    apply_symmetry(scene, lattice, selected_point_indexes, points)

    check_vertex_movement.previous_positions = points


def is_same_point(point1: list[float], point2: list[float]) -> bool:
    return (
        math.isclose(
            point1[0],
            point2[0],
            abs_tol=bpy.context.preferences.addons[__name__].preferences.threshold,
        )
        and math.isclose(
            point1[1],
            point2[1],
            abs_tol=bpy.context.preferences.addons[__name__].preferences.threshold,
        )
        and math.isclose(
            point1[2],
            point2[2],
            abs_tol=bpy.context.preferences.addons[__name__].preferences.threshold,
        )
    )


def find_same_point(
    points: list[list[float]], target_point: list[float]
) -> tuple[list[list[float]], list[int]]:
    result: list[list[float]] = []
    indexes: list[int] = []
    for index, current_point in enumerate(points):
        if is_same_point(current_point, target_point):
            result.append(current_point)
            indexes.append(index)
    return (result, indexes)


def find_symmetric_point(lattice: bpy.types.Lattice, axis: str) -> dict[int, list[int]]:
    selected_points = [
        [i[0], i[1], i[2]]
        for i in [p.co_deform.copy() for p in lattice.points if p.select]
    ]
    points = [[i[0], i[1], i[2]] for i in [p.co_deform.copy() for p in lattice.points]]
    symmetric_map = {}
    for i, point in enumerate(selected_points):
        (_, indexes) = find_same_point(points, convert_to_symmetric_point(point, axis))
        if len(indexes) == 0:
            continue
        symmetric_map[i] = indexes
    return symmetric_map


def convert_to_symmetric_point(point: list[float], axis: str) -> list[float]:
    if axis == "X":
        return [-point[0], point[1], point[2]]
    elif axis == "Y":
        return [point[0], -point[1], point[2]]
    elif axis == "Z":
        return [point[0], point[1], -point[2]]
    else:
        raise ValueError(f"Invalid axis: {axis}")


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
