from ableton.v2.control_surface.elements import EncoderElement
from .nonpackutils import getScriptPath, create_crashlog

class AbsoluteEncoderElement(EncoderElement):
    def normalize_value(self, value):
        create_crashlog(value)
        return value

    def set_light(self, value):
        pass
