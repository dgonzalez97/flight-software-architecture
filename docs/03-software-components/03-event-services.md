### 3.3 Event Services

Event Services provide a standard way for applications to report operational and diagnostic events.

Applications use event identifiers and event types rather than independent `printf()` implementations. Representative event classes are:

- Debug
- Information
- Warning
- Error
- Critical fault

During flatsat and AIT, events may be displayed on a UART or CLI console by a diagnostic application. In flight, the same events may be:

- Sent through Telemetry Output
- Stored by Data Storage
- Used by Health Monitoring
- Filtered by event identifier
- Rate-limited

A typical application call is based on the cFE EVS API, for example:

```c
CFE_EVS_SendEvent(
    PROPULSION_TIMEOUT_EID,
    CFE_EVS_EventType_ERROR,
    "Propulsion response timeout, state=%u",
    (unsigned int)state);
```

Event generation must be rate-limited so that a failing device cannot saturate the telemetry link or consume excessive CPU time.

Table Services may be used to configure which event IDs are enabled, filtered or forwarded. This allows detailed debug information to be enabled for a specific subsystem during a contact without rebuilding the flight image.

Early boot failures that occur before Event Services are available should be written to a small system log or persistent boot record. cFE Executive Services provides a system-log mechanism for events that occur before EVS can be trusted.
