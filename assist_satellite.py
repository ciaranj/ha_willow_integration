"""Platform for light integration."""

from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

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
            Willow(device["label"], device["mac_addr"])
            for device in config_entry.runtime_data
        ]
    )


class Willow(Entity):
    """Representation of a Willow Unit."""

    def __init__(self, name, mac) -> None:
        """Initialize an a Willow entity."""
        self._name = name
        self._attr_unique_id = mac

    @property
    def name(self) -> str:
        """Return the name of this willow satellite."""
        return self._name

    @property
    def device_info(self) -> DeviceInfo:
        """Return the device info."""
        return DeviceInfo(identifiers={(DOMAIN, self._attr_unique_id)}, name=self._name)
