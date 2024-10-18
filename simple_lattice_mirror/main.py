import bpy

from .log import log
from .points import (
    convert_to_symmetric_point,
    find_symmetric_point,
)
from .preferences import get_toggle, get_axis


def is_lattice_mirror_enabled() -> bool:
    """
    Check if the lattice mirror is enabled
    """
    return get_toggle()


def is_lattice_object(obj) -> bool:
    """
    Check if the object is a lattice
    """
    return obj and obj.type == "LATTICE"


def get_lattice_points(
    lattice: bpy.types.Lattice,
) -> tuple[list[int], list[list[float]]]:
    """
    Get the lattice points
    """
    selected_point_indexes = [i for i, p in enumerate(lattice.points) if p.select]
    points = [[i[0], i[1], i[2]] for i in [p.co_deform.copy() for p in lattice.points]]
    return (selected_point_indexes, points)


def is_scene_updated(_, points: list[list[float]], selected_points: list[int]) -> bool:
    """
    Check if the scene is updated
    """
    return (
        (not hasattr(tick, "previous_positions"))
        or (not hasattr(tick, "previous_selections"))
        or (not hasattr(tick, "symmetric_map"))
        or len(tick.previous_positions) != len(points)
        or tick.previous_selections != selected_points
        or tick.axis != get_axis()
    )


def apply_symmetry(
    _,
    lattice: bpy.types.Lattice,
    selected_point_indexes: list[int],
    points: list[list[float]],
) -> None:
    """
    Apply symmetry to the lattice points
    """
    log(f"Selected point indexes: {selected_point_indexes}")
    for i, pointIndex in enumerate(selected_point_indexes):
        if points[pointIndex] == tick.previous_selections[i]:
            continue
        log(
            f"Vertex {pointIndex} has moved from {tick.previous_positions[pointIndex]} to {points[pointIndex]}"
        )
        log(f"Symmetric map: {tick.symmetric_map[i]}")
        for symmetric_index in tick.symmetric_map[i]:
            if symmetric_index in selected_point_indexes:
                continue
            target_symmetric_point = convert_to_symmetric_point(
                points[pointIndex], get_axis()
            )
            target_deform = lattice.points[symmetric_index].co_deform
            target_deform[0] = target_symmetric_point[0]
            target_deform[1] = target_symmetric_point[1]
            target_deform[2] = target_symmetric_point[2]
            points[symmetric_index] = target_symmetric_point
            log(f"Update point {symmetric_index} to {target_deform}")


def tick(scene) -> None:
    """
    process the lattice points on each tick
    """
    obj = bpy.context.active_object
    if not is_lattice_mirror_enabled() or not is_lattice_object(obj):
        return
    lattice: bpy.types.Lattice = obj.data
    (selected_point_indexes, points) = get_lattice_points(lattice)

    if is_scene_updated(scene, points, selected_point_indexes):
        log("Initialize previous_positions")
        tick.previous_positions = points
        tick.previous_selections = selected_point_indexes
        tick.axis = get_axis()
        tick.symmetric_map = find_symmetric_point(lattice, get_axis())

    apply_symmetry(scene, lattice, selected_point_indexes, points)

    tick.previous_positions = points
