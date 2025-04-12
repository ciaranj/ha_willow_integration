"""Dumb Willow integration."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    CONF_HOST,
    CONF_PASSWORD,
    CONF_PORT,
    CONF_USERNAME,
    Platform,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

PLATFORMS: list[Platform] = [
    Platform.ASSIST_SATELLITE,
]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Android IP Webcam from a config entry."""
    # websession = async_get_clientsession(hass)
    # cam = PyDroidIPCam(
    #     websession,
    #     entry.data[CONF_HOST],
    #     entry.data[CONF_PORT],
    #     username=entry.data.get(CONF_USERNAME),
    #     password=entry.data.get(CONF_PASSWORD),
    #     ssl=False,
    # )
    #    coordinator = AndroidIPCamDataUpdateCoordinator(hass, entry, cam)
    #   await coordinator.async_config_entry_first_refresh()

    #  entry.runtime_data = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
