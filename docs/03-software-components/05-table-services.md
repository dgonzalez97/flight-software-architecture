### 3.5 Table Services

Table Services manage configuration data that may change during the mission without recompiling the software.

Examples include:

- AOCS gains
- Sensor calibration data
- Health thresholds
- Rate-of-change thresholds
- Fault persistence values
- Communication timeouts
- Subsystem addresses
- Telemetry selection and rate configuration
- Mode-transition parameters
- Propulsion constraints
- Scheduler definitions
- Event filters

Tables contain configuration, not operational telemetry. Applications may generate telemetry reporting the active table version, validation status or selected parameter values, but telemetry messages are not themselves stored in cFE tables.

Each table should have:

- Version information
- Size
- Integrity check
- Compatibility identifier
- Validation function
- Default values
- Fallback behaviour

The application normally reads the active table during operation. Ground or an onboard application can load an inactive candidate table, validate it and request activation. The application controls when the update becomes active so that configuration cannot change at an unsafe point in the control cycle.

This is particularly useful for AOCS gains, FDIR thresholds and communication configuration.
