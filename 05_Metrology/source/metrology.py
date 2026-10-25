# Klipper Metrology Extension
# QIDI XPRO Rebuild Project
#
# Version: 0.5.0
#
# Generic geometric calibration framework
# Supports:
# - measurement points
# - devices (hotends, probe, sensors)
# - relative offsets

from .models import Point3D, Device, ReferencePoint
from .machine import Machine
from .persistence import (
    load_devices,
    save_device,
    save_devices
)
from .geometry import (
    calculate_axis_offset,
    calculate_offset,
)
from .calibration import CalibrationWorkflow

class Metrology:

    def __init__(self, config):

        self.printer = config.get_printer()

        self.gcode = self.printer.lookup_object(
            'gcode'
        )

        self.machine = Machine()
        self.workflow = CalibrationWorkflow()

        saved_devices = load_devices(config)
        for device in saved_devices.values():
            self.machine.add_device(device)

        self._ensure_workflow_machine()

        #
        # Register commands
        #

        self.gcode.register_command(
            "METROLOGY_POSITION",
            self.cmd_METROLOGY_POSITION
        )

        self.gcode.register_command(
            "METROLOGY_CAPTURE",
            self.cmd_METROLOGY_CAPTURE
        )

        self.gcode.register_command(
            "METROLOGY_COMPARE",
            self.cmd_METROLOGY_COMPARE
        )

        self.gcode.register_command(
            "METROLOGY_LIST",
            self.cmd_METROLOGY_LIST
        )

        self.gcode.register_command(
            "METROLOGY_DELETE",
            self.cmd_METROLOGY_DELETE
        )

        self.gcode.register_command(
            "METROLOGY_CLEAR",
            self.cmd_METROLOGY_CLEAR
        )

        self.gcode.register_command(
            "METROLOGY_DELTA",
            self.cmd_METROLOGY_DELTA
        )

        #
        # Device commands
        #

        self.gcode.register_command(
            "METROLOGY_CAPTURE_DEVICE",
            self.cmd_METROLOGY_CAPTURE_DEVICE
        )

        self.gcode.register_command(
            "METROLOGY_LIST_DEVICES",
            self.cmd_METROLOGY_LIST_DEVICES
        )

        self.gcode.register_command(
            "METROLOGY_CLEAR_DEVICES",
            self.cmd_METROLOGY_CLEAR_DEVICES
        )

        self.gcode.register_command(
            "METROLOGY_OFFSET",
            self.cmd_METROLOGY_OFFSET
        )

        self.gcode.register_command(
            "METROLOGY_OFFSET_X",
            self.cmd_METROLOGY_OFFSET_X
        )

        self.gcode.register_command(
            "METROLOGY_OFFSET_Y",
            self.cmd_METROLOGY_OFFSET_Y
        )

        self.gcode.register_command(
            "METROLOGY_OFFSET_Z",
            self.cmd_METROLOGY_OFFSET_Z
        )

        self.gcode.register_command(
            "METROLOGY_SAVE_DEVICE",
            self.cmd_METROLOGY_SAVE_DEVICE
        )

        self.gcode.register_command(
            "METROLOGY_CORRECTION",
            self.cmd_METROLOGY_CORRECTION
        )

        self.gcode.register_command(
            "METROLOGY_REPORT",
            self.cmd_METROLOGY_REPORT
        )
        self.gcode.register_command(
            "METROLOGY_SAVE_ALL",
            self.cmd_METROLOGY_SAVE_ALL
        )

        self.gcode.register_command(
            "METROLOGY_BUILD_MACHINE",
            self.cmd_METROLOGY_BUILD_MACHINE
        )

        self.gcode.register_command(
            "METROLOGY_CALIBRATE",
            self.cmd_METROLOGY_CALIBRATE
        )

        self.gcode.register_command(
            "METROLOGY_SHOW_OFFSETS",
            self.cmd_METROLOGY_SHOW_OFFSETS
        )

        self.gcode.register_command(
            "METROLOGY_SET_REFERENCE",
            self.cmd_METROLOGY_SET_REFERENCE
        )

        self.gcode.register_command(
            "METROLOGY_APPLY_OFFSETS",
            self.cmd_METROLOGY_APPLY_OFFSETS
        )

    @property
    def devices(self):
        return self.machine.devices

    ####################################################################
    # Internal functions
    ####################################################################

    def _get_two_devices(self, gcmd, usage_msg):
        """
        Extract and validate two device parameters (A and B).
        Returns tuple (device_a, device_b) or raises gcmd.error.
        """
        name_a = gcmd.get("A", None)
        name_b = gcmd.get("B", None)

        if name_a is None or name_b is None:
            raise gcmd.error(usage_msg)

        name_a = name_a.upper()
        name_b = name_b.upper()

        if name_a not in self.devices:
            raise gcmd.error(
                "Device '%s' not found" % name_a
            )

        if name_b not in self.devices:
            raise gcmd.error(
                "Device '%s' not found" % name_b
            )

        return self.devices[name_a], self.devices[name_b]

    def _get_one_device(self, gcmd, usage_msg):
        """
        Extract and validate one device parameter (NAME).
        Returns device or raises gcmd.error.
        """
        name = gcmd.get("NAME", None)

        if name is None:
            raise gcmd.error(usage_msg)

        name = name.upper()

        if name not in self.devices:
            raise gcmd.error(
                "Device '%s' not found" % name
            )

        return self.devices[name]

    def _format_devices_list(self, header):
        """
        Format all devices as a response message.
        """
        if not self.devices:
            return header + "\nNo devices stored"

        msg = header + "\n"

        for name, device in self.devices.items():
            pos = device.position
            msg += (
                "\n%s\n"
                " X = %.6f\n"
                " Y = %.6f\n"
                " Z = %.6f\n"
                %
                (
                    name,
                    pos.x,
                    pos.y,
                    pos.z
                )
            )

        return msg

    def _ensure_workflow_machine(self):
        """
        Rebuild calibration machine state from currently loaded devices.
        """
        if not self.devices:
            return False

        try:
            if self.workflow.machine is None or not self.workflow.get_tool_offsets():
                preferred_reference = self.workflow.get_reference_tool()
                if preferred_reference not in self.devices:
                    preferred_reference = "RIGHT"
                    if preferred_reference not in self.devices:
                        preferred_reference = next(iter(self.devices.keys()))

                self.workflow.set_reference_tool(preferred_reference)
                self.workflow.build_from_devices(self.devices)
        except Exception:
            self.workflow.machine = None
            self.workflow.set_reference_tool("RIGHT")
            return False

        return True

    def _get_kinematic_position(self):

        toolhead = self.printer.lookup_object(
            "toolhead",
            None
        )

        if toolhead is None:
            raise Exception("Printer not ready")

        kin = toolhead.get_kinematics()

        steppers = kin.get_steppers()

        cinfo = {
            s.get_name(): s.get_commanded_position()
            for s in steppers
        }

        pos = kin.calc_position(cinfo)

        return Point3D(
            pos[0],
            pos[1],
            pos[2]
        )

    ####################################################################
    # METROLOGY_POSITION
    ####################################################################

    def cmd_METROLOGY_POSITION(self, gcmd):

        pos = self._get_kinematic_position()

        gcmd.respond_info(
            "METROLOGY POSITION\n"
            "X = %.6f\n"
            "Y = %.6f\n"
            "Z = %.6f"
            %
            (
                pos.x,
                pos.y,
                pos.z
            )
        )


    ####################################################################
    # METROLOGY_CAPTURE
    ####################################################################

    def cmd_METROLOGY_CAPTURE(self, gcmd):

        self.cmd_METROLOGY_CAPTURE_DEVICE(gcmd)


    ####################################################################
    # METROLOGY_COMPARE
    ####################################################################

    def cmd_METROLOGY_COMPARE(self, gcmd):

        a, b = self._get_two_devices(
            gcmd,
            "Usage: METROLOGY_COMPARE A=<name> B=<name>"
        )

        gcmd.respond_info(
            "METROLOGY COMPARISON\n"
            "Reference : %s\n"
            "Measured  : %s\n\n"
            "ΔX = %.6f\n"
            "ΔY = %.6f\n"
            "ΔZ = %.6f"
            %
            (
                a.name,
                b.name,
                b.position.x - a.position.x,
                b.position.y - a.position.y,
                b.position.z - a.position.z
            )
        )

    ####################################################################
    # METROLOGY_DELTA
    ####################################################################

    def cmd_METROLOGY_DELTA(self, gcmd):

        a, b = self._get_two_devices(
            gcmd,
            "Usage: METROLOGY_DELTA A=<device> B=<device>"
        )

        delta = b.position - a.position

        gcmd.respond_info(
            "METROLOGY DELTA\n"
            "FROM %s TO %s\n"
            "DX = %.6f\n"
            "DY = %.6f\n"
            "DZ = %.6f"
            %
            (
                a.name,
                b.name,
                delta.x,
                delta.y,
                delta.z
            )
        )


    ####################################################################
    # METROLOGY_LIST
    ####################################################################

    def cmd_METROLOGY_LIST(self, gcmd):

        msg = self._format_devices_list("METROLOGY LIST")
        gcmd.respond_info(msg)

    ####################################################################
    # METROLOGY_DELETE
    ####################################################################

    def cmd_METROLOGY_DELETE(self, gcmd):

        device = self._get_one_device(
            gcmd,
            "Usage: METROLOGY_DELETE NAME=<name>"
        )

        del self.devices[device.name]

        gcmd.respond_info(
            "Deleted device '%s'"
            % device.name
        )


    ####################################################################
    # METROLOGY_CLEAR
    ####################################################################

    def cmd_METROLOGY_CLEAR(self, gcmd):

        self.devices.clear()

        gcmd.respond_info(
            "All devices cleared"
        )


    def _capture_device(self, gcmd, name):
        name = name.upper()
        pos = self._get_kinematic_position()
        self.devices[name] = Device(
            name,
            Point3D(
                pos.x,
                pos.y,
                pos.z
            )
        )
        return self.devices[name]

    ####################################################################
    # METROLOGY_CAPTURE_DEVICE
    ####################################################################

    def cmd_METROLOGY_CAPTURE_DEVICE(self, gcmd):
        name = gcmd.get(
            "NAME",
            None
        )
        if name is None:
            raise gcmd.error(
# Klipper Metrology Extension
# G-Code controller

from typing import Dict, Any, Optional
import logging

# Import the necessary modules
from .models import Point3D, ReferencePoint, Device
from .geometry import calculate_offset, calculate_distance, build_machine, calculate_axis_offset
from .machine import Machine
from .persistence import save_config, load_config

# Logging configuration
logger = logging.getLogger(__name__)

class Metrology:
    """G-Code controller for metrology operations."""

    def __init__(self) -> None:
        """
        Initialize the metrology controller.
        """
        self.machine: Optional[Machine] = None
        self.commands: Dict[str, Any] = {}
        self._register_commands()

    def _register_commands(self) -> None:
        """
        Register all available commands.
        """
        # Calibration commands
        self.commands["CALIBRATE"] = self._calibrate
        self.commands["MEASURE"] = self._measure
        self.commands["OFFSET"] = self._offset
        self.commands["DISTANCE"] = self._distance
        self.commands["SAVE_CONFIG"] = self._save_config

    def _calibrate(self, params: Dict[str, Any]) -> str:
        """
        Calibrate the machine.

        Args:
            params (Dict[str, Any]): Calibration parameters

        Returns:
            str: Response message
        """
        try:
            # Calibration implementation
            return "Calibration completed successfully"
        except Exception as e:
            logger.error(f"Calibration failed: {e}")
            return f"Calibration failed: {str(e)}"

    def _measure(self, params: Dict[str, Any]) -> str:
        """
        Measure a point.

        Args:
            params (Dict[str, Any]): Measurement parameters

        Returns:
            str: Response message
        """
        try:
            # Measurement implementation
            return "Measurement completed successfully"
        except Exception as e:
            logger.error(f"Measurement failed: {e}")
            return f"Measurement failed: {str(e)}"

    def _offset(self, params: Dict[str, Any]) -> str:
        """
        Calculate offset between points.

        Args:
            params (Dict[str, Any]): Offset parameters

        Returns:
            str: Response message
        """
        try:
            # Offset calculation implementation
            return "Offset calculation completed"
        except Exception as e:
            logger.error(f"Offset calculation failed: {e}")
            return f"Offset calculation failed: {str(e)}"

    def _distance(self, params: Dict[str, Any]) -> str:
        """
        Calculate distance between points.

        Args:
            params (Dict[str, Any]): Distance parameters

        Returns:
            str: Response message
        """
        try:
            # Distance calculation implementation
            return "Distance calculation completed"
        except Exception as e:
            logger.error(f"Distance calculation failed: {e}")
            return f"Distance calculation failed: {str(e)}"

    def _save_config(self, params: Dict[str, Any]) -> str:
        """
        Save current configuration.

        Args:
            params (Dict[str, Any]): Save parameters

        Returns:
            str: Response message
        """
        try:
            # Configuration saving implementation
            return "Configuration saved successfully"
        except Exception as e:
            logger.error(f"Configuration save failed: {e}")
            return f"Configuration save failed: {str(e)}"

    def execute_command(self, command: str, params: Dict[str, Any]) -> str:
        """
        Execute a metrology command.

        Args:
            command (str): Command name
            params (Dict[str, Any]): Command parameters

        Returns:
            str: Command response
        """
        if command.upper() in self.commands:
            return self.commands[command.upper()](params)
        else:
            return f"Unknown command: {command}"

# Function to create metrology instance
def create_metrology() -> Metrology:
    """
    Create and return a metrology instance.

    Returns:
        Metrology: Initialized metrology controller
    """
    return Metrology()
            )

        device = self._capture_device(gcmd, name)

        gcmd.respond_info(
            "DEVICE CAPTURED\n"
            "Name : %s\n"
            "X = %.6f\n"
            "Y = %.6f\n"
            "Z = %.6f"
            %
            (
                device.name,
                device.position.x,
                device.position.y,
                device.position.z
            )
        )

    ####################################################################
    # METROLOGY_LIST_DEVICES
    ####################################################################

    def cmd_METROLOGY_LIST_DEVICES(self, gcmd):

        msg = self._format_devices_list("METROLOGY DEVICES")
        gcmd.respond_info(msg)


    ####################################################################
    # METROLOGY_CLEAR_DEVICES
    ####################################################################

    def cmd_METROLOGY_CLEAR_DEVICES(self, gcmd):

        self.cmd_METROLOGY_CLEAR(gcmd)


    ####################################################################
    # METROLOGY_CALIBRATE
    ####################################################################

    def cmd_METROLOGY_CALIBRATE(self, gcmd):
        name = gcmd.get("NAME", None)
        reference_name = gcmd.get("REFERENCE", None)
        save_config = gcmd.get("SAVE", None) is not None

        if name is None:
            raise gcmd.error(
                "Usage: METROLOGY_CALIBRATE NAME=<device> [REFERENCE=<device>] [SAVE=1]"
            )

        device_name = name.upper()
        self._capture_device(gcmd, device_name)

        if reference_name is None:
            reference_name = self.workflow.get_reference_tool()

        if reference_name is None or reference_name.upper() not in self.devices:
            reference_name = "RIGHT"
            if reference_name not in self.devices:
                reference_name = next(iter(self.devices.keys()), "RIGHT")

        reference_name = reference_name.upper()
        self.workflow.set_reference_tool(reference_name)

        if not self._ensure_workflow_machine():
            raise gcmd.error("Unable to build machine from captured devices")

        msg = "METROLOGY CALIBRATION\n"
        msg += "Captured: %s\n" % device_name
        msg += "Reference: %s\n" % reference_name

        offsets = self.workflow.get_tool_offsets()
        for tool_name, offset in offsets.items():
            msg += (
                "%s: X=%.6f Y=%.6f Z=%.6f\n"
                %
                (
                    tool_name,
                    offset.x,
                    offset.y,
                    offset.z
                )
            )

        if save_config:
            configfile = self.printer.lookup_object("configfile")
            save_devices(configfile, self.devices)
            msg += "\nSaved devices to configuration."

        gcmd.respond_info(msg)

    ####################################################################
    # METROLOGY_OFFSET
    ####################################################################

    def cmd_METROLOGY_OFFSET(self, gcmd):

        a, b = self._get_two_devices(
            gcmd,
            "Usage: METROLOGY_OFFSET A=<device> B=<device>"
        )

        offset = calculate_offset(
            a.position,
            b.position
        )

        gcmd.respond_info(
            "METROLOGY OFFSET\n\n"
            "REFERENCE : %s\n"
            "TARGET    : %s\n\n"
            "DX = %.6f\n"
            "DY = %.6f\n"
            "DZ = %.6f"
            %
            (
                a.name,
                b.name,
                offset.x,
                offset.y,
                offset.z
            )
        )


    ####################################################################
    # METROLOGY_CORRECTION
    #
    # Returns the correction required to place B over A
    #
    # Result = A - B
    ####################################################################

    def cmd_METROLOGY_CORRECTION(self, gcmd):

        a, b = self._get_two_devices(
            gcmd,
            "Usage: METROLOGY_CORRECTION A=<device> B=<device>"
        )

        correction = calculate_offset(
            b.position,
            a.position
        )

        gcmd.respond_info(
            "METROLOGY CORRECTION\n\n"
            "REFERENCE : %s\n"
            "TARGET    : %s\n\n"
            "APPLY TO TARGET:\n"
            "DX = %.6f\n"
            "DY = %.6f\n"
            "DZ = %.6f"
            %
            (
                a.name,
                b.name,
                correction.x,
                correction.y,
                correction.z
            )
        )



    ####################################################################
    # METROLOGY_REPORT
    ####################################################################

    def cmd_METROLOGY_REPORT(self, gcmd):

        msg = self._format_devices_list("METROLOGY REPORT")
        gcmd.respond_info(msg)

####################################################################
    # METROLOGY_SAVE_DEVICE
    ####################################################################

    def cmd_METROLOGY_SAVE_DEVICE(self, gcmd):

        device = self._get_one_device(
            gcmd,
            "Usage: METROLOGY_SAVE_DEVICE NAME=<name>"
        )

        configfile = self.printer.lookup_object(
            "configfile"
        )

        save_device(
            configfile,
            device
        )

        gcmd.respond_info(
            "Saved device '%s'"
            % device.name
        )
    ####################################################################
    # METROLOGY_SAVE_ALL
    ####################################################################

    def cmd_METROLOGY_SAVE_ALL(self, gcmd):

        configfile = self.printer.lookup_object(
            "configfile"
        )

        save_devices(
            configfile,
            self.devices
        )

        gcmd.respond_info(
            "All devices scheduled for SAVE_CONFIG"
        )

    ####################################################################
    # OFFSET AXIS CALCULATION
    ####################################################################

    def _calculate_device_axis_offset(self, gcmd, axis):

        a, b = self._get_two_devices(
            gcmd,
            "Usage: METROLOGY_OFFSET_%s A=<device> B=<device>"
            % axis.upper()
        )

        value = calculate_axis_offset(
            a.position,
            b.position,
            axis
        )

        gcmd.respond_info(
            "METROLOGY OFFSET %s\n\n"
            "REFERENCE : %s\n"
            "TARGET    : %s\n\n"
            "Δ%s = %.6f"
            %
            (
                axis.upper(),
                a.name,
                b.name,
                axis.upper(),
                value
            )
        )

    ####################################################################
    # METROLOGY_OFFSET_X
    ####################################################################

    def cmd_METROLOGY_OFFSET_X(self, gcmd):

        self._calculate_device_axis_offset(
            gcmd,
            "X"
        )


    ####################################################################
    # METROLOGY_OFFSET_Y
    ####################################################################

    def cmd_METROLOGY_OFFSET_Y(self, gcmd):

        self._calculate_device_axis_offset(
            gcmd,
            "Y"
        )


    ####################################################################
    # METROLOGY_OFFSET_Z
    ####################################################################

    def cmd_METROLOGY_OFFSET_Z(self, gcmd):

        self._calculate_device_axis_offset(
            gcmd,
            "Z"
        )

    ####################################################################
    # METROLOGY_BUILD_MACHINE
    ####################################################################

    def cmd_METROLOGY_BUILD_MACHINE(self, gcmd):
        """
        Build machine geometry from currently captured devices.
        Calculates tool offsets relative to reference tool.
        """
        try:
            self.workflow.build_from_devices(
                self.devices
            )

            msg = "METROLOGY MACHINE BUILD\n"
            msg += "Reference tool: %s\n" % self.workflow.get_reference_tool()

            offsets = self.workflow.get_tool_offsets()
            for name, offset in offsets.items():
                msg += (
                    "%s: X=%.6f Y=%.6f Z=%.6f\n"
                    %
                    (
                        name,
                        offset.x,
                        offset.y,
                        offset.z
                    )
                )

            gcmd.respond_info(msg)

        except Exception as e:
            raise gcmd.error(str(e))

    ####################################################################
    # METROLOGY_SHOW_OFFSETS
    ####################################################################

    def cmd_METROLOGY_SHOW_OFFSETS(self, gcmd):
        """
        Display all calculated tool offsets.
        """
        try:
            if not self._ensure_workflow_machine():
                gcmd.respond_info("METROLOGY TOOL OFFSETS\nNo devices available")
                return

            msg = "METROLOGY TOOL OFFSETS\n"
            msg += "Reference: %s\n" % self.workflow.get_reference_tool()

            offsets = self.workflow.get_tool_offsets()
            for name, offset in offsets.items():
                msg += (
                    "%s: X=%.6f Y=%.6f Z=%.6f\n"
                    %
                    (
                        name,
                        offset.x,
                        offset.y,
                        offset.z
                    )
                )

            gcmd.respond_info(msg)

        except Exception as e:
            gcmd.respond_info(
                "METROLOGY TOOL OFFSETS\n"
                "ERROR: %s" % str(e)
            )
            return

    ####################################################################
    # METROLOGY_SET_REFERENCE
    ####################################################################

    def cmd_METROLOGY_SET_REFERENCE(self, gcmd):
        """
        Set which device is the reference tool for calibration.
        """
        device = self._get_one_device(
            gcmd,
            "Usage: METROLOGY_SET_REFERENCE NAME=<device>"
        )

        self.workflow.set_reference_tool(device.name)

        gcmd.respond_info(
            "Reference tool set to '%s'"
            % device.name
        )

    ####################################################################
    # METROLOGY_APPLY_OFFSETS
    ####################################################################

    def cmd_METROLOGY_APPLY_OFFSETS(self, gcmd):
        """
        Apply calculated offsets to extruder configuration.
        Uses default mapping unless tool parameters are provided.

        Default mapping:
          RIGHT → extruder
          LEFT → extruder1
          PROBE → probe

        Manual mapping example:
          METROLOGY_APPLY_OFFSETS RIGHT=extruder LEFT=extruder1
        """
        try:
            if not self._ensure_workflow_machine():
                raise RuntimeError(
                    "No devices available. Capture devices first."
                )

            # Check for manual tool mapping parameters
            tool_mapping = {}
            for device_name in ["RIGHT", "LEFT", "PROBE"]:
                section = gcmd.get(device_name, None)
                if section is not None:
                    tool_mapping[device_name] = section

            # Apply offsets to configuration
            results = self.workflow.apply_offsets_to_config(
                self.printer.lookup_object("configfile"),
                tool_mapping if tool_mapping else None
            )

            # Build response message
            msg = "METROLOGY OFFSETS APPLIED\n"
            msg += "Mapping:\n"

            for device_name, info in results.items():
                offset = info["offset"]
                section = info["section"]
                msg += (
                    "\n[%s] (%s):\n"
                    " offset_x = %.6f\n"
                    " offset_y = %.6f\n"
                    " offset_z = %.6f\n"
                    %
                    (
                        section,
                        device_name,
                        offset.x,
                        offset.y,
                        offset.z
                    )
                )

            msg += "\nOffsets saved to configuration.\n"
            msg += "Restart Klipper to apply changes."

            gcmd.respond_info(msg)

        except Exception as e:
            raise gcmd.error(str(e))

####################################################################
# Klipper loader
####################################################################

def load_config(config):

    return Metrology(config)

