# Klipper Metrology Extension
# Data models

from typing import Optional, Dict, Any
from dataclasses import dataclass

############################################################
# Point3D
############################################################
class Point3D:
    """Represents a 3D point in space with x, y, z coordinates."""

    def __init__(self, x: float = 0.0, y: float = 0.0, z: float = 0.0) -> None:
        """
        Initialize a 3D point.

        Args:
            x (float): X coordinate
            y (float): Y coordinate
            z (float): Z coordinate
        """
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def __add__(self, other: 'Point3D') -> 'Point3D':
        """Add two Point3D objects."""
        if not isinstance(other, Point3D):
            return NotImplemented
        return Point3D(
            self.x + other.x,
            self.y + other.y,
            self.z + other.z
        )

    def __sub__(self, other: 'Point3D') -> 'Point3D':
        """Subtract two Point3D objects."""
        if not isinstance(other, Point3D):
            return NotImplemented
        return Point3D(
            self.x - other.x,
            self.y - other.y,
            self.z - other.z
        )

    def __eq__(self, other: object) -> bool:
        """Check equality with another Point3D object."""
        if not isinstance(other, Point3D):
            return NotImplemented
        return (
            self.x == other.x and
            self.y == other.y and
            self.z == other.z
        )

    def __repr__(self) -> str:
        """String representation of the Point3D."""
        return (
            f"Point3D("
            f"x={self.x:.6f}, "
            f"y={self.y:.6f}, "
            f"z={self.z:.6f})"
        )

    def as_dict(self) -> Dict[str, float]:
        """Convert Point3D to dictionary representation."""
        return {
            "x": self.x,
            "y": self.y,
            "z": self.z
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Point3D':
        """
        Create Point3D from dictionary.

        Args:
            data (Dict[str, Any]): Dictionary with x, y, z keys

        Returns:
            Point3D: New Point3D instance
        """
        return cls(
            data["x"],
            data["y"],
            data["z"]
        )

############################################################
# ReferencePoint
############################################################
#
# Represents any physical point measured.
#
# Examples:
#
# BED_ORIGIN
# HOTEND_RIGHT
# HOTEND_LEFT
#
############################################################

class ReferencePoint:
    """Represents a physical reference point measured in the system."""

    def __init__(self, name: str, position: Optional[Point3D] = None) -> None:
        """
        Initialize a reference point.

        Args:
            name (str): Name of the reference point
            position (Optional[Point3D]): Position of the point, defaults to origin
        """
        self.name = name.upper()
        if position is None:
            position = Point3D()
        self.position = position

############################################################
# Device
############################################################
#
# Maintained for compatibility.
#
# It may be replaced in the future by ReferencePoint definitively.
#
############################################################

class Device(ReferencePoint):
    """Represents a measurement device (legacy compatibility)."""

    def __init__(self, name: str, position: Optional[Point3D] = None) -> None:
        """
        Initialize a device.

        Args:
            name (str): Name of the device
            position (Optional[Point3D]): Position of the device, defaults to origin
        """
        super().__init__(name, position)