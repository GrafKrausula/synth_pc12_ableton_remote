from __future__ import absolute_import, print_function, unicode_literals
import logging
from ableton.v2.control_surface.elements import ButtonElement
from ableton.v2.control_surface import midi, MIDI_NOTE_TYPE

logger = logging.getLogger(__name__)


class NoteButtonElement(ButtonElement):
    def __init__(self, *a, **k):
        super(NoteButtonElement, self).__init__(True, MIDI_NOTE_TYPE, *a, **k)

    def _do_send_value(self, value, channel=None):
        data_byte1 = self._original_identifier
        data_byte2 = value

        channel = self._original_channel if channel is None else channel
        status = midi.NOTE_OFF_STATUS if value == 0 else midi.NOTE_ON_STATUS
        status_byte = channel + status

        # logger.info(u'send value (channel={},status={},identifier={},value={})'.format(channel, status, self._original_identifier, value))

        if self.send_midi((status_byte, data_byte1, data_byte2)):
            self._last_sent_message = (value, channel)
            if self._report_output:
                is_input = True
                self._report_value(value, not is_input)

    def receive_value(self, value):
        last_sent_value = self._last_sent_value
        do_send_value = value == 0 and last_sent_value >= 0
        super(NoteButtonElement, self).receive_value(value)
        if do_send_value:
            self._do_send_value(last_sent_value)
