# Klipper Metrology Extension
# Calibration workflows

from .models import Point3D
from .geometry import calculate_offset, build_machine
from .machine import Machine


class CalibrationWorkflow:
    """
    Manages calibration workflows and offset application.
    """

    def __init__(self):
        """
        Initialize calibration state.
        """
        self.reference_tool = "RIGHT"
        self.corrections = {}
        self.machine = None

    def build_from_devices(self, devices, bed_size_x=235.0, bed_size_y=160.0):
        """
        Build machine geometry from captured devices.
        Calculates tool offsets relative to reference tool.
        """
        if not devices:
            raise ValueError("No devices available")

        reference = self.reference_tool.upper()
        if reference not in devices:
            raise ValueError(
                f"Reference tool '{reference}' not found in devices"
            )

        self.machine = build_machine(
            devices,
            reference=reference,
            bed_size_x=bed_size_x,
            bed_size_y=bed_size_y
        )

        return self.machine

    def get_tool_offsets(self):
        """
        Return all tool offsets from the built machine.
        """
        if self.machine is None:
            return {}

        return self.machine.tool_offsets

    def get_tool_offset(self, name):
        """
        Get offset for a specific tool.
        """
        if self.machine is None:
            return Point3D()

        return self.machine.get_tool_offset(name)

    def set_reference_tool(self, name):
        """
        Set which tool is the reference for calibration.
        """
        self.reference_tool = name.upper()

    def get_reference_tool(self):
        """
        Get the current reference tool name.
        """
        return self.reference_tool

    def apply_offsets_to_config(self, configfile, tool_mapping=None):
        """
        Apply calculated tool offsets to printer configuration.
        Saves offsets to each tool's config section.

        Args:
            configfile: Klipper configfile object
            tool_mapping: dict of {device_name: config_section}
                         e.g., {"RIGHT": "extruder", "LEFT": "extruder1"}
                         If None, uses default mapping.
        """
        if self.machine is None:
            raise RuntimeError("Machine not built yet")

        # Default mapping
        default_mapping = {
            "RIGHT": "extruder",
            "LEFT": "extruder1",
            "PROBE": "probe"
        }

        if tool_mapping is None:
            tool_mapping = default_mapping
        else:
            # Merge with defaults for unmapped tools
            merged = default_mapping.copy()
            merged.update(tool_mapping)
            tool_mapping = merged

        offsets = self.machine.tool_offsets
        results = {}

        for device_name, offset in offsets.items():
            if device_name not in tool_mapping:
                continue

            config_section = tool_mapping[device_name]

            # Only apply to sections that should have offsets
            if device_name == "PROBE":
                # Probe might have special handling, but we apply offset_z
                configfile.set(
                    config_section,
                    "offset_x",
                    "%.6f" % offset.x
                )
                configfile.set(
                    config_section,
                    "offset_y",
                    "%.6f" % offset.y
                )
                configfile.set(
                    config_section,
                    "offset_z",
                    "%.6f" % offset.z
                )
            else:
                # For extruders (RIGHT, LEFT, etc.)
                configfile.set(
                    config_section,
                    "offset_x",
                    "%.6f" % offset.x
                )
                configfile.set(
                    config_section,
                    "offset_y",
                    "%.6f" % offset.y
                )
                configfile.set(
                    config_section,
                    "offset_z",
                    "%.6f" % offset.z
                )

            results[device_name] = {
                "section": config_section,
                "offset": offset
            }

        return results
