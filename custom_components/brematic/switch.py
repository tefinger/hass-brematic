import logging

import voluptuous as vol

# Import the device class from the component that you want to support
from homeassistant.components.switch import (
    ENTITY_ID_FORMAT,
    PLATFORM_SCHEMA,
    SwitchEntity,
)
from homeassistant.const import CONF_FRIENDLY_NAME, CONF_HOST, CONF_SWITCHES, STATE_ON
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.restore_state import RestoreEntity

from .const import (
    VERSION,
    CONF_SYSTEM_CODE,
    CONF_GATEWAY_TYPE,
    CONF_UNIT_CODE,
    CONF_UNIT_TYPE,
    GATEWAY_TYPE_BRENNENSTUHL,
    GATEWAY_TYPE_INTERTECHNO,
    GATEWAY_TYPES,
    UNIT_TYPE_RCS1000N,
    UNIT_TYPE_RCR1000N,
    UNIT_TYPE_AB440SA,
    UNIT_TYPE_CMR300,
    UNIT_TYPE_CMR500,
    UNIT_TYPE_CMR1000,
    UNIT_TYPE_ITR300,
    UNIT_TYPE_ITR3500,
    UNIT_TYPE_PAR1500,
    UNIT_TYPES,
    DEFAULT_UNIT_TYPE,
    DEFAULT_GATEWAY_TYPE,
)

_LOGGER = logging.getLogger(__name__)


# Validation of the user's configuration
UNIT_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_UNIT_CODE): cv.string,
        vol.Optional(CONF_UNIT_TYPE, default=DEFAULT_UNIT_TYPE): vol.In(UNIT_TYPES),
        vol.Optional(CONF_FRIENDLY_NAME): cv.string,
    }
)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_HOST): cv.string,
        vol.Optional(CONF_GATEWAY_TYPE, default=DEFAULT_GATEWAY_TYPE): vol.In(
            GATEWAY_TYPES
        ),
        vol.Required(CONF_SYSTEM_CODE): cv.string,
        vol.Required(CONF_SWITCHES): vol.Schema({cv.slug: UNIT_SCHEMA}),
    }
)


def get_gateway(gateway_type, host):
    """Prepare the gateway"""
    if gateway_type == GATEWAY_TYPE_BRENNENSTUHL:
        from pyBrematic.gateways import BrennenstuhlGateway

        return BrennenstuhlGateway(host)
    elif gateway_type == GATEWAY_TYPE_INTERTECHNO:
        from pyBrematic.gateways import IntertechnoGateway

        return IntertechnoGateway(host)


def get_unit(system_code, unit_conf):
    """Prepares the device"""
    unit_type = unit_conf.get(CONF_UNIT_TYPE)
    unit_code = unit_conf.get(CONF_UNIT_CODE)

    if unit_type == UNIT_TYPE_RCS1000N:
        from pyBrematic.devices.brennenstuhl import RCS1000N

        return RCS1000N(system_code, unit_code)
    elif unit_type == UNIT_TYPE_RCR1000N:
        from pyBrematic.devices.brennenstuhl import RCR1000N

        return RCR1000N(system_code, unit_code)
    elif unit_type == UNIT_TYPE_AB440SA:
        from pyBrematic.devices.elro import AB440SA

        return AB440SA(system_code, unit_code)
    elif unit_type == UNIT_TYPE_CMR300:
        from pyBrematic.devices.intertechno import CMR300

        return CMR300(system_code, unit_code)
    elif unit_type == UNIT_TYPE_CMR500:
        from pyBrematic.devices.intertechno import CMR500

        return CMR500(system_code, unit_code)
    elif unit_type == UNIT_TYPE_CMR1000:
        from pyBrematic.devices.intertechno import CMR1000

        return CMR1000(system_code, unit_code)
    elif unit_type == UNIT_TYPE_ITR300:
        from pyBrematic.devices.intertechno import ITR300

        return ITR300(system_code, unit_code)
    elif unit_type == UNIT_TYPE_ITR3500:
        from pyBrematic.devices.intertechno import ITR3500

        return ITR3500(system_code, unit_code)
    elif unit_type == UNIT_TYPE_PAR1500:
        from pyBrematic.devices.intertechno import PAR1500

        return PAR1500(system_code, unit_code)


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Setup the Brematic platform."""

    host = config.get(CONF_HOST)
    system_code = config.get(CONF_SYSTEM_CODE)
    gateway_type = config.get(CONF_GATEWAY_TYPE)

    gateway = get_gateway(gateway_type, host)

    # Add units
    devices = config.get(CONF_SWITCHES, {})
    switches = []

    for object_id, device_config in devices.items():
        unit = get_unit(system_code, device_config)
        switches.append(
            BrematicSwitch(
                hass,
                object_id,
                gateway,
                unit,
                device_config.get(CONF_FRIENDLY_NAME, object_id),
            )
        )

    if not switches:
        _LOGGER.error("No switches added")
        return False

    add_entities(switches)


class BrematicSwitch(SwitchEntity, RestoreEntity):
    """Representation a switch that can be toggled using Brematic Gateway"""

    def __init__(self, hass, object_id, gateway, unit, friendly_name):
        """Initialize the switch."""
        self._hass = hass
        self.entity_id = ENTITY_ID_FORMAT.format(object_id)
        self._name = friendly_name
        self._gateway = gateway
        self._unit = unit

    async def async_added_to_hass(self):
        """Restore Brematic device state (ON/OFF)."""
        await super().async_added_to_hass()

        old_state = await self.async_get_last_state()
        if old_state is not None:
            self._state = old_state.state == STATE_ON
        else:
            self._state = False

    @property
    def should_poll(self):
        """Do not poll."""
        return False

    @property
    def name(self):
        """Return the name of the switch."""
        return self._name

    @property
    def is_on(self):
        """Return true if device is on."""
        return self._state

    @property
    def assumed_state(self):
        """Return true if unable to access real state of entity."""
        return True

    def turn_on(self, **kwargs):
        """Turn the device on."""
        from pyBrematic.devices import Device

        self._gateway.send_request(self._unit, Device.ACTION_ON)
        self._state = True
        self.schedule_update_ha_state()

    def turn_off(self, **kwargs):
        """Turn the device off."""
        from pyBrematic.devices import Device

        self._gateway.send_request(self._unit, Device.ACTION_OFF)
        self._state = False
        self.schedule_update_ha_state()
