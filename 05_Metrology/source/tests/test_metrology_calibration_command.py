import sys
import unittest
from types import SimpleNamespace

sys.path.insert(0, "/opt/3dprinter/klipper/klippy/extras")

from metrology.metrology import Metrology


class DummySection:
    def __init__(self, values):
        self.values = values

    def get_prefix_options(self, prefix):
        return [k for k in self.values if k.startswith(prefix)]

    def getfloat(self, option, default=0.0):
        return float(self.values.get(option, default))


class DummyConfig:
    def __init__(self):
        self.values = {
            "device_right_x": 14.999223,
            "device_right_y": 3.994874,
            "device_right_z": -1.0,
            "device_left_x": 39.896036,
            "device_left_y": 3.805144,
            "device_left_z": -1.0,
            "device_probe_x": 34.003860,
            "device_probe_y": 6.998935,
            "device_probe_z": 155.0,
        }
        self.printer = None

    def get_printer(self):
        return self.printer

    def getsection(self, name):
        return DummySection(self.values)


class DummyGcode:
    def __init__(self):
        self.commands = {}
        self.responses = []

    def register_command(self, name, callback):
        self.commands[name] = callback

    def respond_info(self, msg):
        self.responses.append(msg)

    def error(self, msg):
        raise RuntimeError(msg)


class DummyToolhead:
    def get_kinematics(self):
        class Kin:
            def get_steppers(self):
                return []

            def calc_position(self, cinfo):
                return (10.0, 20.0, 30.0)

        return Kin()


class DummyPrinter:
    def __init__(self, config, gcode):
        self.config = config
        self.gcode = gcode

    def lookup_object(self, name, default=None):
        if name == "gcode":
            return self.gcode
        if name == "toolhead":
            return DummyToolhead()
        if name == "configfile":
            return SimpleNamespace(set=lambda *args, **kwargs: None, remove_option=lambda *args, **kwargs: None)
        return default


class FakeGcmd:
    def __init__(self, values):
        self.values = values
        self.responses = []

    def get(self, name, default=None):
        return self.values.get(name, default)

    def respond_info(self, msg):
        self.responses.append(msg)

    def error(self, msg):
        raise RuntimeError(msg)


class TestMetrologyCalibrationCommand(unittest.TestCase):
    def test_calibrate_command_captures_device_and_reports_offsets(self):
        config = DummyConfig()
        gcode = DummyGcode()
        printer = DummyPrinter(config, gcode)
        config.printer = printer

        metrology = Metrology(config)
        gcmd = FakeGcmd({"NAME": "LEFT", "APPLY": "1"})

        metrology.cmd_METROLOGY_CALIBRATE(gcmd)

        response = "\n".join(gcmd.responses)
        self.assertIn("METROLOGY CALIBRATION", response)
        self.assertIn("LEFT", response)
        self.assertIn("X=", response)


if __name__ == "__main__":
    unittest.main()
