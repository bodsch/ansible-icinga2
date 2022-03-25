# timeperiods

To set up a proper notification, corresponding TimePeriod objects are required.

The following objects are created by default:
- never
- 9to5
- 24x7

```yaml
icinga2_defaults_timeperiod:
  never:
    display_name: Icinga2 never TimePeriod
    ranges: {}

  9to5:
    display_name: Icinga2 9to5 TimePeriod
    ranges:
      monday: "09:00-17:00"
      tuesday: "09:00-17:00"
      wednesday: "09:00-17:00"
      thursday: "09:00-17:00"
      friday: "09:00-17:00"
      saturday: "09:00-17:00"
      sunday: "09:00-17:00"

  24x7:
    display_name: Icinga2 24x7 TimePeriod
    ranges:
      monday: "00:00-24:00"
      tuesday: "00:00-24:00"
      wednesday: "00:00-24:00"
      thursday: "00:00-24:00"
      friday: "00:00-24:00"
      saturday: "00:00-24:00"
      sunday: "00:00-24:00"
```
