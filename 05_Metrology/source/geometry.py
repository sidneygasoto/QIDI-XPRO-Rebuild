# Klipper Metrology Extension
# Geometry operations

from typing import Dict, Any
from .models import Point3D
from .machine import Machine

def calculate_offset(reference: Point3D, target: Point3D) -> Point3D:
    """
    Calculate the offset between two points.

    Args:
        reference (Point3D): Reference point
        target (Point3D): Target point

    Returns:
        Point3D: Offset vector from reference to target
    """
    return Point3D(
        target.x - reference.x,
        target.y - reference.y,
        target.z - reference.z
    )

def calculate_distance(a: Point3D, b: Point3D) -> float:
    """
    Calculate the Euclidean distance between two points.

    Args:
        a (Point3D): First point
        b (Point3D): Second point

    Returns:
        float: Distance between the points
    """
    dx = b.x - a.x
    dy = b.y - a.y
    dz = b.z - a.z
    return (
        dx * dx +
        dy * dy +
        dz * dz
    ) ** 0.5

####################################################################
# Machine builder
####################################################################
def build_machine(
    devices: Dict[str, Any],
    reference: str = "RIGHT",
    bed_size_x: float = 235.0,
    bed_size_y: float = 160.0
) -> Machine:
    """
    Build a machine configuration from device measurements.

    Args:
        devices (Dict[str, Any]): Dictionary of devices with their positions
        reference (str): Reference device name (defaults to "RIGHT")
        bed_size_x (float): Bed size in X direction
        bed_size_y (float): Bed size in Y direction

    Returns:
        Machine: Configured machine object

    Raises:
        ValueError: If reference device is not found
    """
    reference = reference.upper()
    if reference not in devices:
        raise ValueError(
            f"Reference device '{reference}' not found"
        )
    machine = Machine()

    #
    # Register devices
    #
    for device in devices.values():
        machine.add_device(
            device
        )
    machine.set_reference_tool(
        reference
    )
    ref = devices[reference]

    #
    # Printable area origin
    #
    machine.set_bed_origin(
        Point3D(
            ref.position.x,
            ref.position.y,
            0.0
        )
    )

    #
    # Printable dimensions
    #
    machine.set_bed_size(
        bed_size_x,
        bed_size_y
    )

    #
    # Tool offsets
    #
    for name, device in devices.items():
        offset = calculate_offset(
            ref.position,
            device.position
        )
        machine.set_tool_offset(
            name,
            offset
        )

    return machine

################################################################
# Axis offset
################################################################
def calculate_axis_offset(reference: Point3D, target: Point3D, axis: str) -> float:
    """
    Calculate the offset in a single axis.

    Args:
        reference (Point3D): Reference point
        target (Point3D): Target point
        axis (str): Axis name ("x", "y", or "z")

    Returns:
        float: Offset value in the specified axis

    Raises:
        ValueError: If axis is not valid
    """
    axis = axis.lower()
    if axis not in ("x", "y", "z"):
        raise ValueError(f"Invalid axis '{axis}'")
    return (
        getattr(target, axis)
        - getattr(reference, axis)
    )