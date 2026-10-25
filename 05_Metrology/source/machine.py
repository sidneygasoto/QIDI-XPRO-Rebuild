# Klipper Metrology Extension
# Machine geometry model

from typing import Optional, Dict, Any
from .models import Point3D


class Machine:
    """Machine geometry model representing the physical configuration."""

    def __init__(self) -> None:
        """
        Initialize the machine model.
        """
        #
        # Registered devices
        #
        self.devices: Dict[str, Any] = {}

        #
        # Printable area origin
        #
        self.bed_origin: Point3D = Point3D()

        #
        # Printable dimensions
        #
        self.bed_size: Point3D = Point3D()

        #
        # Tool offsets
        #
        self.tool_offsets: Dict[str, Point3D] = {}

        #
        # Reference tool
        #
        self.reference_tool: Optional[str] = None


    ####################################################################
    # Bed
    ####################################################################

    def set_bed_origin(self, point: Point3D) -> None:
        """
        Set the bed origin point.

        Args:
            point (Point3D): Origin point of the printable area
        """
        self.bed_origin = point


    def set_bed_size(self, x: float, y: float) -> None:
        """
        Set the bed size dimensions.

        Args:
            x (float): Bed size in X direction
            y (float): Bed size in Y direction
        """
        self.bed_size = Point3D(
            x,
            y,
            0.0
        )


    ####################################################################
    # Reference tool
    ####################################################################

    def set_reference_tool(self, name: str) -> None:
        """
        Set the reference tool name.

        Args:
            name (str): Name of the reference tool
        """
        self.reference_tool = name.upper()


    def get_reference_tool(self) -> Optional[str]:
        """
        Get the reference tool name.

        Returns:
            Optional[str]: Name of the reference tool, or None if not set
        """
        return self.reference_tool


    def get_reference_device(self) -> Optional[Any]:
        """
        Get the reference device.

        Returns:
            Optional[Any]: Reference device object, or None if not set
        """
        if self.reference_tool is None:
            return None

        return self.get_device(
            self.reference_tool
        )


    ####################################################################
    # Tool offsets
    ####################################################################

    def set_tool_offset(self, name: str, offset: Point3D) -> None:
        """
        Set the tool offset for a device.

        Args:
            name (str): Name of the device/tool
            offset (Point3D): Offset vector for the tool
        """
        self.tool_offsets[
            name.upper()
        ] = offset


    def get_tool_offset(self, name: str) -> Point3D:
        """
        Get the tool offset for a device.

        Args:
            name (str): Name of the device/tool

        Returns:
            Point3D: Offset vector for the tool, or zero point if not found
        """
        return self.tool_offsets.get(
            name.upper(),
            Point3D()
        )


    ####################################################################
    # Queries
    ####################################################################

    def has_reference_tool(self) -> bool:
        """
        Check if a reference tool is set.

        Returns:
            bool: True if reference tool is set, False otherwise
        """
        return self.reference_tool is not None


    def has_tool(self, name: str) -> bool:
        """
        Check if a tool exists in the configuration.

        Args:
            name (str): Name of the tool to check

        Returns:
            bool: True if tool exists, False otherwise
        """
        return (
            name.upper()
            in self.tool_offsets
        )


    ####################################################################
    # Devices
    ####################################################################

    def add_device(self, device: Any) -> None:
        """
        Add a device to the machine configuration.

        Args:
            device (Any): Device object to add
        """
        self.devices[
            device.name
        ] = device


    def get_device(self, name: str) -> Optional[Any]:
        """
        Get a device by name.

        Args:
            name (str): Name of the device to retrieve

        Returns:
            Optional[Any]: Device object, or None if not found
        """
        return self.devices.get(
            name.upper()
        )


    def get_devices(self) -> Dict[str, Any]:
        """
        Get all registered devices.

        Returns:
            Dict[str, Any]: Dictionary of all devices
        """
        return self.devices


    def remove_device(self, name: str) -> None:
        """
        Remove a device from the configuration.

        Args:
            name (str): Name of the device to remove
        """
        self.devices.pop(
            name.upper(),
            None
        )


    def clear_devices(self) -> None:
        """
        Clear all registered devices.
        """
        self.devices.clear()
