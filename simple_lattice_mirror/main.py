import bpy

from .log import log
from .points import (
    convert_to_symmetric_point,
    find_symmetric_point,
)
from .preferences import get_toggle, get_axis


def is_lattice_mirror_enabled() -> bool:
    return get_toggle()


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
        or check_vertex_movement.axis != get_axis()
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
                points[pointIndex], get_axis()
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
        check_vertex_movement.axis = get_axis()
        check_vertex_movement.symmetric_map = find_symmetric_point(lattice, get_axis())

    apply_symmetry(scene, lattice, selected_point_indexes, points)

    check_vertex_movement.previous_positions = points
