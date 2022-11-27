import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import sensor, ble_client

from esphome.const import (
    CONF_BATTERY_LEVEL,
    CONF_TEMPERATURE,
    CONF_ID,
    DEVICE_CLASS_BATTERY,
    DEVICE_CLASS_TEMPERATURE,
    ENTITY_CATEGORY_DIAGNOSTIC,
    STATE_CLASS_MEASUREMENT,
    UNIT_PERCENT,
    UNIT_CELSIUS,
)

DEPENDENCIES = ["ble_client"]

igrill_ns = cg.esphome_ns.namespace("igrill")
IGrill = igrill_ns.class_(
    "IGrill", cg.PollingComponent, ble_client.BLEClientNode
)

CONF_HAS_PROPANE_LEVEL = "has_propane_level"

CONFIG_SCHEMA = cv.All(
    cv.Schema(
        {
            cv.GenerateID(): cv.declare_id(IGrill),
            cv.Optional(CONF_BATTERY_LEVEL): sensor.sensor_schema(
                unit_of_measurement=UNIT_PERCENT,
                accuracy_decimals=0,
                device_class=DEVICE_CLASS_BATTERY,
                state_class=STATE_CLASS_MEASUREMENT,
                entity_category=ENTITY_CATEGORY_DIAGNOSTIC,
            ),
            cv.Optional(CONF_TEMPERATURE): sensor.sensor_schema(
                unit_of_measurement=UNIT_CELSIUS,
                accuracy_decimals=2,
                device_class=DEVICE_CLASS_TEMPERATURE,
                state_class=STATE_CLASS_MEASUREMENT,
            ),
            cv.Optional(CONF_HAS_PROPANE_LEVEL, default=False): cv.boolean,
        }
    )
    .extend(cv.polling_component_schema("5min"))
    .extend(ble_client.BLE_CLIENT_SCHEMA),
)


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)

    await ble_client.register_ble_node(var, config)

    if CONF_BATTERY_LEVEL in config:
        sens = await sensor.new_sensor(config[CONF_BATTERY_LEVEL])
        cg.add(var.set_battery(sens))
    if CONF_TEMPERATURE in config:
        sens = await sensor.new_sensor(config[CONF_TEMPERATURE])
        cg.add(var.set_temperature(sens))
    cg.add(var.set_has_propane_level(config[CONF_HAS_PROPANE_LEVEL]))