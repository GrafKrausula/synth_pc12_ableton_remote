from __future__ import absolute_import, print_function, unicode_literals
try:
  # Python 3
  from itertools import zip_longest
except ImportError:
  from itertools import izip_longest as zip_longest
from ableton.v2.control_surface.components import MixerComponent as MixerComponentBase

from .channel_strip_component import ChannelStripComponent

class MixerComponent(MixerComponentBase):

    def __init__(self, *a, **k):
        super(MixerComponent, self).__init__(channel_strip_component_type=ChannelStripComponent, *a, **k)

    def set_send_controls(self, controls):
        self._send_controls = controls
        for strip, control in zip_longest(self._channel_strips, controls or []):
            if self._send_index is None:
                strip.set_send_controls(None)
            else:
                strip.set_send_controls(control)

    def set_monitor_buttons(self, buttons):
        for strip, button in zip_longest(self._channel_strips, buttons or []):
            strip.set_monitor_button(button)

    def set_launch_clip_buttons(self, buttons):
        for strip, button in zip_longest(self._channel_strips, buttons or []):
            strip.set_launch_clip_button(button)

    def set_stop_buttons(self, buttons):
        for strip, button in zip_longest(self._channel_strips, buttons or []):
            strip.set_stop_button(button)
    