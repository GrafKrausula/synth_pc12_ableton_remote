from __future__ import absolute_import, print_function, unicode_literals
import Live

from .utils import getScriptPath, create_crashlog
import sys, traceback, pathlib
from pathlib import Path

import logging
#import subprocess
#from subprocess import *
#from subprocess import Popen, PIPE
#from subprocess import Popen, CREATE_NEW_CONSOLE

from ableton.v2.base import depends, inject
from ableton.v2.control_surface.elements import MultiElement, EncoderElement, SliderElement, ButtonElement
from ableton.v2.control_surface import MIDI_CC_TYPE, MIDI_NOTE_TYPE, CompoundElement


from .note_button_element import NoteButtonElement
from .pitch_bend_element import PitchBendElement
from .absolute_encoder_element import AbsoluteEncoderElement
from .consts import *


logger = logging.getLogger(__name__)


@depends(skin=None)
def create_button(channel, identifier, name, **k):
    button = NoteButtonElement(channel, identifier, name=name, **k)
    button.set_feedback_delay(-1)
    return button


def create_encoder(channel, identifier, name, map_mode=Live.MidiMap.MapMode.absolute):
    Element = AbsoluteEncoderElement if map_mode == Live.MidiMap.MapMode.absolute else EncoderElement
    encoder = Element(MIDI_CC_TYPE, channel, identifier, map_mode, name=name)
    create_crashlog([MIDI_CC_TYPE, channel, identifier, map_mode, name])
    if map_mode != Live.MidiMap.MapMode.absolute:
        encoder.set_feedback_delay(-1)
    #create_crashlog(dir(EncoderElement))
    #create_crashlog(encoder.mapped_parameter())
    #create_crashlog(encoder._last_sent_value)
    return encoder


def create_slider(channel, identifier, name):
    slider = SliderElement(MIDI_CC_TYPE, channel, identifier, name=name)
    return slider


def numbers(base):
    return ((index, FaderfoxUniversal_CH1 + (index // 8), base + (index % 8)) for index in range(NUMBER_TRACKS))


def button_base(base, name):
    return CompoundElement(
        control_elements=[
            create_button(channel, identifier, name + u'_{}'.format(index))
            for (index, channel, identifier) in numbers(base)
        ],
        name=name + u'_Buttons',
    )


def encoder_base(base, name):
    return CompoundElement(
        control_elements=[
            create_encoder(channel, identifier, name + u'_{}'.format(index))
            for (index, channel, identifier) in numbers(base)
        ],
        name=name + u'_Encoders',
    )


def slider_base(base, name):
    return CompoundElement(
        control_elements=[
            create_slider(channel, identifier,
                          name=name + u'_{}'.format(index))
            for (index, channel, identifier) in numbers(base)
        ],
        name=name + u'_Sliders',
    )


def send_element_row(index, channel, identifier):
    return CompoundElement(
        control_elements=[
            create_encoder(channel, CC_TRACK_SEND1_BASE +
                           identifier, u'Send1_Encoder_{}'.format(index)),
            create_encoder(channel, CC_TRACK_SEND2_BASE +
                           identifier, u'Send2_Encoder_{}'.format(index)),
            create_encoder(channel, CC_TRACK_SEND3_BASE +
                           identifier, u'Send3_Encoder_{}'.format(index)),
            create_encoder(channel, CC_TRACK_SEND4_BASE +
                           identifier, u'Send4_Encoder_{}'.format(index)),
        ],
        name=u'Send_Encoders_{}'.format(index),
    )


class MultiEncoderElement(CompoundElement):
    def send_value(self, value):
        for control in self.owned_control_elements():
            control.send_value(value)

    def normalize_value(self, value):
        return self.owned_control_elements()[0].normalize_value(value)


class FaderfoxElements:
    def __init__(self):
        try:
            self.track_select_buttons = button_base(
                NOTE_SELECT_TRACK_BASE, u'Track_Select')
            # self.mute_buttons = button_base(NOTE_MUTE_TRACK_BASE, u'Mute')
            # self.arm_buttons = button_base(NOTE_ARM_TRACK_BASE, u'Arm')
            # self.monitor_buttons = button_base(NOTE_MONITOR_TRACK_BASE, u'Monitor')
            # self.solo_buttons = button_base(NOTE_SOLO_TRACK_BASE, u'Solo')
            #
            # self.volume_encoders = slider_base(CC_TRACK_VOLUME_BASE, u'Volume')
            # self.pan_encoders = encoder_base(CC_TRACK_PAN_BASE, u'Pan')
            # self.send_encoders = CompoundElement(
            #     control_elements=[send_element_row(index, channel, identifier) for (
            #         index, channel, identifier) in numbers(0)],
            #     name=u'Send_Encoders'
            # )

            self._macro_encoders_raw = [
                create_encoder(
                    FaderfoxUniversal_CH1, CC_MACRO_BASE_SELECTED_TRACK + index, u'Macro_{}'
                )
                for index in range(16)
            ]

            create_crashlog(self._macro_encoders_raw)


            self.macro_encoders = CompoundElement(
                control_elements=self._macro_encoders_raw, name=u'Macro_Encoders'
            )

            # self.selected_send_encoders = CompoundElement(
            #     control_elements=[
            #         create_encoder(
            #             FaderfoxUniversal_CH2,
            #             CC_SEND_SELECTED_TRACK_BASE +
            #             index if index < 3 else CC_HIGH_SEND_SELECTED_TRACK_BASE + index - 3,
            #             u'Selected_Send_{}'.format(index),
            #         )
            #         for index in range(12)
            #     ],
            #     name=u'Selected_Send_Encoders',
            # )

            # self.selected_pan_encoder = create_encoder(
            #     FaderfoxUniversal_CH2, CC_PAN_SELECTED_TRACK, u'Selected_Pan'
            # )
            # self.selected_volume_encoder = create_encoder(
            #     FaderfoxUniversal_CH2, CC_VOLUME_SELECTED_TRACK, u'Selected_Volume'
            # )
            #
            # self.selected_arm_button = create_button(
            #     FaderfoxUniversal_CH2, NOTE_ARM_SELECTED, u'Selected_Arm'
            # )
            # self.selected_monitor_button = create_button(
            #     FaderfoxUniversal_CH2, NOTE_MONITOR_SELECTED, u'Selected_Monitor'
            # )
            # self.selected_solo_button = create_button(
            #     FaderfoxUniversal_CH2, NOTE_SOLO_SELECTED, u'Selected_Solo'
            # )
            # self.selected_mute_button = create_button(
            #     FaderfoxUniversal_CH2, NOTE_MUTE_SELECTED, u'Selected_Mute'
            # )
            #
            # self.scene_select_encoder = MultiEncoderElement(control_elements=[
            #     create_encoder(FaderfoxUniversal_CH1, CC_SCENE_SELECT, u'Select_Scene_CH1',
            #                    Live.MidiMap.MapMode.relative_smooth_two_compliment),
            #     create_encoder(FaderfoxUniversal_CH2, CC_SCENE_SELECT, u'Select_Scene_CH2',
            #                    Live.MidiMap.MapMode.relative_smooth_two_compliment)
            # ], name=u'Select_Scene')
            #
            # self.track_select_encoder = MultiEncoderElement(control_elements=[
            #     create_encoder(FaderfoxUniversal_CH1, CC_TRACK_SELECT, u'Select_Track_CH1',
            #                    Live.MidiMap.MapMode.relative_smooth_two_compliment),
            #     create_encoder(FaderfoxUniversal_CH2, CC_TRACK_SELECT, u'Select_Track_CH2',
            #                    Live.MidiMap.MapMode.relative_smooth_two_compliment),
            # ], name=u'Select_Track')

            # self.track_view_button = create_button(
            #     FaderfoxUniversal_CH2, NOTE_TRACK_VIEW, u'Track_View')
            # self.clip_view_button = create_button(
            #     FaderfoxUniversal_CH2, NOTE_CLIP_VIEW, u'Clip_View')
            #
            # self.launch_clip_button = create_button(
            #     FaderfoxUniversal_CH2, NOTE_LAUNCH_CLIP_SELECTED, u'Launch_Clip')
            # self.stop_track_button = create_button(
            #     FaderfoxUniversal_CH2, NOTE_STOP_CLIP_SELECTED, u'Stop_Track')
            #
            # self.launch_clip_buttons = button_base(
            #     NOTE_LAUNCH_TRACK_BASE, u'Launch_Clip')
            # self.stop_track_buttons = button_base(
            #     NOTE_STOP_TRACK_BASE, u'Stop_Track')
            #
            # self.tempo_coarse_encoder = create_encoder(
            #     FaderfoxUniversal_CH1,
            #     CC_TEMPO_COARSE,
            #     u'Tempo_Coarse',
            #     Live.MidiMap.MapMode.relative_smooth_two_compliment,
            # )
            # self.tempo_fine_encoder = create_encoder(
            #     FaderfoxUniversal_CH1,
            #     CC_TEMPO_FINE,
            #     u'Tempo_Fine',
            #     Live.MidiMap.MapMode.relative_smooth_two_compliment,
            # )
            #
            # self.play_button = create_button(
            #     FaderfoxUniversal_CH1, NOTE_GLOBAL_PLAY, u'Global_Play')
            # self.stop_button = create_button(
            #     FaderfoxUniversal_CH1, NOTE_GLOBAL_STOP, u'Global_Stop')
            # self.record_button = create_button(
            #     FaderfoxUniversal_CH1, NOTE_GLOBAL_RECORD, u'Global_Record')
            #
            # self.nudge_up_button = create_button(
            #     FaderfoxUniversal_CH1, NOTE_NUDGE_UP, u'Nudge_Up')
            # self.nudge_down_button = create_button(
            #     FaderfoxUniversal_CH1, NOTE_NUDGE_DOWN, u'Nudge_Down')
            #
            # self.master_pan_encoder = create_encoder(
            #     FaderfoxUniversal_CH1, CC_MASTER_PAN, u'Master_Pan')
            # self.master_volume_encoder = create_encoder(
            #     FaderfoxUniversal_CH1, CC_MASTER_VOLUME, u'Master_Volume')
            # self.cue_volume_encoder = create_encoder(
            #     FaderfoxUniversal_CH1, CC_CUE_VOLUME, u'Cue_Volume')
            #
            # self.arranger_view_button = create_button(
            #     FaderfoxUniversal_CH1, NOTE_SWITCH_ARRANGEMENT_VIEW, u'Arranger_View')
            # self.launch_selected_scene_button = create_button(
            #     FaderfoxUniversal_CH1, NOTE_START_SCENE, u'Launch_Selected_Scene')
            # self.stop_selected_scene_button = create_button(
            #     FaderfoxUniversal_CH1, NOTE_STOP_SCENE, u'Stop_Selected_Scene')
            #
            # self.quantization_encoder = create_encoder(
            #     FaderfoxUniversal_CH1, CC_QUANTIZATION, u'Clip_Quantization')
            #
            # self.pitch_bend = PitchBendElement(FaderfoxUniversal_CH1)
            #
            # self.crossfader = create_slider(
            #     FaderfoxUniversal_CH2, CC_CROSSFADE, u'Crossfader')
            #
            # self.crossfader_assign = AbsoluteEncoderElement(
            #     MIDI_CC_TYPE, FaderfoxUniversal_CH2, CC_CROSSFADER_ASSIGN, Live.MidiMap.MapMode.absolute, name=u'Crossfader_Assign')

        except Exception as err:
            traceback_string = traceback.format_exc()
            create_crashlog(traceback_string)

            #traceback_string = traceback_string.replace('\n','" & echo "')
            #openScriptCmd = ('cmd /k echo "%s" &' %err)
            #openScriptCmd += ('echo "%s"' %traceback_string)
            #process = subprocess.Popen(openScriptCmd, creationflags=CREATE_NEW_CONSOLE)
