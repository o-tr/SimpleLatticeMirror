import math
import bpy

from .preferences import get_threshold


def is_same_point(point1: list[float], point2: list[float]) -> bool:
    """
    Check if two points are the same
    """
    return (
        math.isclose(
            point1[0],
            point2[0],
            abs_tol=get_threshold(),
        )
        and math.isclose(
            point1[1],
            point2[1],
            abs_tol=get_threshold(),
        )
        and math.isclose(
            point1[2],
            point2[2],
            abs_tol=get_threshold(),
        )
    )


def find_same_point(
    points: list[list[float]], target_point: list[float]
) -> tuple[list[list[float]], list[int]]:
    """
    Find the same point in the list of points
    """
    result: list[list[float]] = []
    indexes: list[int] = []
    for index, current_point in enumerate(points):
        if is_same_point(current_point, target_point):
            result.append(current_point)
            indexes.append(index)
    return (result, indexes)


def find_symmetric_point(lattice: bpy.types.Lattice, axis: str) -> dict[int, list[int]]:
    """
    Find the symmetric points
    """
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
    """
    Convert the point to the symmetric point
    """
    if axis == "X":
        return [-point[0], point[1], point[2]]
    elif axis == "Y":
        return [point[0], -point[1], point[2]]
    elif axis == "Z":
        return [point[0], point[1], -point[2]]
    else:
        raise ValueError(f"Invalid axis: {axis}")
