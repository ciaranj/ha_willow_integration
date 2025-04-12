import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_MAC

from .const import DOMAIN

STEP_USER_DATA_SCHEMA = vol.Schema({vol.Required(CONF_MAC): str})


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Example config flow."""

    # The schema version of the entries that it creates
    # Home Assistant will call your migrate method if the version changes
    VERSION = 1
    MINOR_VERSION = 1

    async def async_step_user(self, user_input):
        data_schema = self.add_suggested_values_to_schema(
            STEP_USER_DATA_SCHEMA,
            user_input,
        )
        if user_input is None:
            return self.async_show_form(step_id="user", data_schema=data_schema)

        await self.async_set_unique_id(f"willow-{user_input[CONF_MAC]}")
        self._abort_if_unique_id_configured()

        return self.async_create_entry(
            title=user_input[CONF_MAC],
            data={CONF_MAC: user_input[CONF_MAC]},
        )
