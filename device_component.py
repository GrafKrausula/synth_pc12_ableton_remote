from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface import ParameterInfo
from ableton.v2.control_surface.components import DeviceComponent as DeviceComponentBase
from .utils import getScriptPath, create_crashlog
import sys, traceback, pathlib
from pathlib import Path

class DeviceComponent(DeviceComponentBase):
    def _create_parameter_info(self, parameter, name):
        create_crashlog(["device_comp.py" ,parameter, name])
        return ParameterInfo(
            parameter=parameter, name=name, default_encoder_sensitivity=1.0
        )
