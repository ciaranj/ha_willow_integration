import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_NAME, CONF_URL

from .const import CONF_ALLOW_INVALID_SSL, DOMAIN

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_NAME): str,
        vol.Required(CONF_URL): str,
        vol.Required(CONF_ALLOW_INVALID_SSL, default=False): bool,
    }
)


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Basic config flow."""

    # The schema version of the entries that it creates
    # Home Assistant will call your migrate method if the version changes
    VERSION = 1
    MINOR_VERSION = 1

    async def async_step_user(self, user_input):
        """Implement a WAS server configuration form."""
        data_schema = self.add_suggested_values_to_schema(
            STEP_USER_DATA_SCHEMA, user_input
        )
        if user_input is None:
            return self.async_show_form(step_id="user", data_schema=data_schema)

        await self.async_set_unique_id(f"willow-was-{user_input[CONF_NAME]}")
        self._abort_if_unique_id_configured()

        return self.async_create_entry(
            title=user_input[CONF_NAME],
            data={
                CONF_URL: user_input[CONF_URL],
                CONF_ALLOW_INVALID_SSL: user_input[CONF_ALLOW_INVALID_SSL],
            },
        )
