"""Platform for light integration."""

from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from homeassistant.components.assist_satellite.entity import AssistSatelliteState

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the available devices from a configured WAS entry."""

    async_add_entities(
        [
            Willow(hass, device["label"], device["mac_addr"], device["platform"], device["version"])
            for device in config_entry.runtime_data
        ]
    )


class Willow(Entity):
    """Representation of a Willow Unit."""

    def __init__(self, hass, name, mac, platform, version) -> None:
        """Initialize an a Willow entity."""
        self._name = name
        self._attr_unique_id = f"{mac}-satellite"
        self._registry = dr.async_get(hass)
        self._deviceidentifier = (DOMAIN, mac)
        self._platform = platform
        self._version = version
        self._attr_state = AssistSatelliteState.IDLE
        hass.bus.async_listen("willow_event", self._handle_event)

    def _handle_event(self, call):
        # TODO: could probably cache the device id for this entity
        # TODO: should probably create a timer that flushes it back to idle periodically
        device = self._registry.async_get(call.data["device_id"])
        if self._deviceidentifier in device.identifiers:
            if call.data["type"] == "wake_start":
                self._attr_state = AssistSatelliteState.LISTENING
            elif call.data["type"] == "wake_end":
                self._attr_state = AssistSatelliteState.PROCESSING
            elif call.data["type"] == "command_finished":
                self._attr_state = AssistSatelliteState.RESPONDING
            elif call.data["type"] == "response_end":
                self._attr_state = AssistSatelliteState.IDLE
            self.schedule_update_ha_state(True)

    @property
    def name(self) -> str:
        """Return the name of this willow satellite."""
        return self._name

    @property
    def device_info(self) -> DeviceInfo:
        """Return the device info."""
        return DeviceInfo(identifiers={self._deviceidentifier}, name=self._name, model=self._platform, sw_version=self._version)
