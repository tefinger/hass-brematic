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
- Intertechno CMR300
- Intertechno CMR500
- Intertechno CMR1000
- Intertechno ITR300
- Intertechno ITR3500
- Intertechno PAR1500

(*) Tested devices

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