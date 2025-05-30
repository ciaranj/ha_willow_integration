# Willow Custom Integration
A simple willow integration, required if you want your willow satellites to be area aware when they run their intent pipelines within Home assistant

## Installation

1. Use [HACS](https://hacs.xyz/docs/setup/download), in `HACS > Integrations > Explore & Add Repositories` search for "Willow". After adding this `https://github.com/ciaranj/ha_willow_integration` as a custom repository. Skip to 7.
2. If you do not have HACS, use the tool of choice to open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
3. If you do not have a `custom_components` directory (folder) there, you need to create it.
4. In the `custom_components` directory (folder) create a new folder called `willow`.
5. Download _all_ the files from the `custom_components/willow/` directory (folder) in this repository.
6. Place the files you downloaded in the new directory (folder) you created.
7. Restart Home Assistant.
8. Add the integration or in the HA UI go to "Settings" -> "Devices & Services" then click "+" and search for "Willow".
