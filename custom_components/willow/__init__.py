"""Dumb Willow integration."""

from __future__ import annotations

import asyncio
from urllib.parse import urljoin

import aiohttp

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_URL, Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import CONF_ALLOW_INVALID_SSL

SETUP_TIMEOUT = 5
REQUIRED_DEVICE_FIELDS = {"label", "mac_addr", "platform", "version"}

PLATFORMS: list[Platform] = [
    Platform.ASSIST_SATELLITE,
]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Willow ApplicationServer from a config entry."""

    session = async_get_clientsession(
        hass,
        verify_ssl=not entry.data[CONF_ALLOW_INVALID_SSL],
    )

    try:
        async with asyncio.timeout(SETUP_TIMEOUT):
            async with session.get(
                urljoin(entry.data[CONF_URL], "/api/client")
            ) as response:
                response.raise_for_status()
                devices = await response.json()
    except (TimeoutError, aiohttp.ClientError, ValueError) as ex:
        raise ConfigEntryNotReady(f"Problem connecting to WAS: {ex}") from ex

    if not isinstance(devices, list) or any(
        not isinstance(device, dict)
        or not REQUIRED_DEVICE_FIELDS <= device.keys()
        for device in devices
    ):
        raise ConfigEntryNotReady(
            "Invalid response from WAS: expected a list of devices"
        )

    entry.runtime_data = devices

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
