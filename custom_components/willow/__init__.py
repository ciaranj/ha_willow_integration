"""Dumb Willow integration."""

from __future__ import annotations

from urllib.parse import urljoin

import aiohttp

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_URL, Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryError

from .const import CONF_ALLOW_INVALID_SSL

PLATFORMS: list[Platform] = [
    Platform.ASSIST_SATELLITE,
]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Willow ApplicationServer from a config entry."""

    j = []
    try:
        async with (
            aiohttp.ClientSession() as session,
            session.get(
                urljoin(entry.data[CONF_URL], "/api/client"),
                ssl=(False if entry.data[CONF_ALLOW_INVALID_SSL] else None),
            ) as resp,
        ):
            j = await resp.json()
    except Exception as ex:
        raise ConfigEntryError(f"Problem connecting to WAS: {ex}") from ex

    entry.runtime_data = j

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
