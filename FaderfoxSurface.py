from __future__ import absolute_import, print_function, unicode_literals
import logging
from ableton.v2.base import depends, inject, const
from ableton.v2.control_surface import (
    ControlSurface,
    DeviceDecoratorFactory,
    Layer,
    BankingInfo,
)
from ableton.v2.control_surface.components import (
    SessionRingComponent,
    ChannelStripComponent,
    SimpleTrackAssigner,
    SessionNavigationComponent,
    DeviceParameterComponent,
)
from ableton.v2.control_surface.default_bank_definitions import BANK_DEFINITIONS
from .device_component import DeviceComponent
from .mixer_component import MixerComponent
from .view_control_component import ViewControlComponent
from .transport_component import TransportComponent

from .utils import getScriptPath, create_crashlog
import sys, traceback, pathlib
from pathlib import Path

from .FaderfoxElements import FaderfoxElements
from .skin_default import default_skin
from .consts import *


logger = logging.getLogger(__name__)

class FaderfoxSurface(ControlSurface):
    __doc__ = u'Faderfox Universal controller script'
    __version__ = u'v0.1'
    __name__ = u'Faderfox Synth PC12'
    __module__ = __name__

    def __init__(self, c_instance):
        ControlSurface.__init__(self, c_instance)

        self._create_elements()
        self._create_components()

        self.show_message(u'{} sadddin {}'.format(self.__name__, self.__version__))

    def _create_elements(self):
        with self.component_guard():
            with inject(skin=const(default_skin)).everywhere():
                self._elements = FaderfoxElements()
                create_crashlog(self._elements)

    def _create_components(self):
        with self.component_guard():
            with inject(element_container=const(self._elements)).everywhere():
                #self._create_mixer()
                #self._create_view_control()
                #self._create_transport()
                self._create_device()

    # def _create_mixer(self):
    #     self._session_ring = SessionRingComponent(
    #         is_enabled=False,
    #         num_tracks=NUMBER_TRACKS,
    #         tracks_to_use=lambda: tuple(
    #             self.song.tracks) + tuple(self.song.return_tracks) + (self.song.master_track,),
    #         name=u'Session_Ring',
    #     )
    #
    #     mixerLayer = Layer(
    #         arm_buttons=u'arm_buttons',
    #         monitor_buttons=u'monitor_buttons',
    #         solo_buttons=u'solo_buttons',
    #         mute_buttons=u'mute_buttons',
    #         launch_clip_buttons=u'launch_clip_buttons',
    #         stop_buttons=u'stop_track_buttons',
    #
    #         track_select_buttons=u'track_select_buttons',
    #         volume_controls=u'volume_encoders',
    #         pan_controls=u'pan_encoders',
    #         send_controls=u'send_encoders',
    #         prehear_volume_control=u'cue_volume_encoder',
    #
    #         crossfader_control=u'crossfader',
    #     )
    #
    #     self._mixer = MixerComponent(
    #         is_enabled=False,
    #         tracks_provider=self._session_ring,
    #         track_assigner=SimpleTrackAssigner(),
    #         name=u'Mixer',
    #         layer=mixerLayer,
    #     )
    #
    #     self._mixer.selected_strip().layer = Layer(
    #         arm_button=u'selected_arm_button',
    #         monitor_button=u'selected_monitor_button',
    #         solo_button=u'selected_solo_button',
    #         mute_button=u'selected_mute_button',
    #         launch_clip_button=u'launch_clip_button',
    #         stop_button=u'stop_track_button',
    #
    #         volume_control=u'selected_volume_encoder',
    #         pan_control=u'selected_pan_encoder',
    #         send_controls=u'selected_send_encoders',
    #         crossfade_toggle=u'crossfader_assign',
    #     )
    #
    #     self._mixer.master_strip().layer = Layer(
    #         volume_control=u'master_volume_encoder',
    #         pan_control=u'master_pan_encoder',
    #     )
    #
    #     # self._session_ring.set_enabled(True)
    #     self._mixer.set_enabled(True)
    #
    # def _create_view_control(self):
    #     viewLayer = Layer(
    #         track_view_button=u'track_view_button',
    #         clip_view_button=u'clip_view_button',
    #         scene_select_encoder=u'scene_select_encoder',
    #         track_select_encoder=u'track_select_encoder',
    #         arranger_view_button=u'arranger_view_button',
    #     )
    #     self._view_control = ViewControlComponent(
    #         is_enabled=False, name=u'View_Control', layer=viewLayer, session_ring=self._session_ring)
    #     self._view_control.set_enabled(True)

    def _create_device(self):

        try:
            self._banking_info = BankingInfo(BANK_DEFINITIONS)
            self._device = DeviceComponent(
                is_enabled=False,
                device_decorator_factory=DeviceDecoratorFactory(),
                device_bank_registry=self._device_bank_registry,
                banking_info=self._banking_info,
                name=u'Device',
            )
            self._device_parameters = DeviceParameterComponent(
                is_enabled=False,
                parameter_provider=self._device,
                name=u'Device_Parameters',
                layer=Layer(parameter_controls=u'macro_encoders'),
            )

            create_crashlog("_banking_info")
            create_crashlog(dir(self._banking_info))

            create_crashlog("device")
            create_crashlog(dir(self._device))

            create_crashlog("device_parameters")
            create_crashlog(dir(self._device_parameters))
            # self._device.set_enabled(True)
            self._device_parameters.set_enabled(True)


            create_crashlog("device_bank_definition")
            create_crashlog(self._banking_info.device_bank_definition(self._device))

            create_crashlog("parameters_listener_count")
            create_crashlog(self._device.parameters_listener_count())

            create_crashlog("device_listener_count")
            create_crashlog(self._device.device_listener_count())

            create_crashlog("enabled_listener_count")
            create_crashlog(self._device_parameters.enabled_listener_count())


        except Exception as err:
            traceback_string = traceback.format_exc()
            create_crashlog(traceback_string)

    # def _create_transport(self):
    #     transportLayer = Layer(
    #         tempo_control=u'tempo_coarse_encoder',
    #         tempo_fine_control=u'tempo_fine_encoder',
    #         tempo_display_control=u'pitch_bend',
    #         play_button=u'play_button',
    #         stop_button=u'stop_button',
    #         record_button=u'record_button',
    #         nudge_up_button=u'nudge_up_button',
    #         nudge_down_button=u'nudge_down_button',
    #         launch_selected_scene_button=u'launch_selected_scene_button',
    #         stop_selected_scene_button=u'stop_selected_scene_button',
    #         quantization_control=u'quantization_encoder',
    #     )
    #     self._transport = TransportComponent(
    #         is_enabled=False, name=u'Transport', layer=transportLayer)
    #     self._transport.set_enabled(True)
