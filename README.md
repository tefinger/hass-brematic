![GitHub release](https://img.shields.io/github/release/tefinger/hass-brematic.svg)
![GitHub](https://img.shields.io/github/license/tefinger/hass-brematic.svg)
![Maintenance](https://img.shields.io/maintenance/yes/2099.svg)
![project stage](https://img.shields.io/badge/project%20stage-work%20in%20progress-green.svg)
![GitHub commit activity](https://img.shields.io/github/commit-activity/y/tefinger/hass-brematic.svg)

# Custom component: Brematic
Custom component for Home Assistant to support Brematic devices.

# Supported devices
## Gateways
- Brennenstuhl (*)
- Intertechno

## Devices
- Brennenstuhl RCS1000N (*)
- Brennenstuhl RCR1000N
- Elro AB440SA
- Intertechno CMR1000
- Intertechno PAR1500

(*) Tested devices

# Installation
There are two ways for installing this custom component. Manually or by using [custom_updater](https://www.home-assistant.io/components/light.switch/).

## Manual installation
- Download this repository to your machine
- Copy the folder `brematic` to `<config>/custom_components/`

## Custom updater
- Make sure you have [custom_updater](https://www.home-assistant.io/components/light.switch/) installed and running
- Add the url for the brematic component to your custom_updater configuration like this:
```yaml
custom_updater:
  component_urls:
    - https://raw.githubusercontent.com/tefinger/hass-brematic/master/custom_updater.json
```

# Configuration
Add the brematic platform as a `switch` to your `configuration.yaml` file.

```yaml
switch:
  - platform: brematic
    host: '10.0.3.2'
    system_code: '01010'
    gateway_type: 'Brennenstuhl'
    switches:
      power_outlet:
        unit_code: '00010'
        friendly_name: Power Outlet
      floor_lamp:
        unit_code: '11111'
        unit_type: 'RCS1000N'
```
**Please note:** only `switch` is supported. If you want to control your power outlet as a `light` please refer to the [light switch](https://www.home-assistant.io/components/light.switch/) component.

## Configuration variables

- **host**<br />&nbsp;&nbsp;*(string) (Required)* Ip address or hostname of the gateway
- **system_code**<br />&nbsp;&nbsp;*(string) (Required)* System code you use for your devices
- **gateway_type**<br />&nbsp;&nbsp;*(string) (Optional)* Type of the gateway (`Brennenstuhl`, `Intertechno`) <br />&nbsp;&nbsp; default: `Brennenstuhl`
- **switches**<br />&nbsp;&nbsp;*(map) (Required)* The array that contains all switches
  - **identifier**<br />&nbsp;&nbsp;*(map) (Required)* Name of the command switch as slug. Multiple entries are possible.
    - **unit_code**<br />&nbsp;&nbsp;*(string) (Required)* Unit code of the device
    - **unit_type**<br />&nbsp;&nbsp;*(string) (Optional)* Type of the unit (`RCS1000N`, `RCR1000N`, `AB440SA`, `CMR1000`, `PAR1500`) <br />&nbsp;&nbsp; default: `RCS1000N`
    - **friendly_name**<br />&nbsp;&nbsp;*(string) (Optional)* Friendly name of the device
