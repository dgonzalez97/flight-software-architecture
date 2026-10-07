### 3.1 Executive Services

Executive Services manage the lifecycle of the cFE applications after the operational or recovery image has started.

The bootloader and Executive Services are related through reset state and startup information, but they are not the same component:

- The bootloader runs before FreeRTOS and cFE and selects the image to execute.
- Executive Services run inside the selected image and manage cFE application startup and lifecycle.
- The Update Manager receives and validates a future image while the operational software is running.

Executive Services are responsible for:

- Application startup order
- Application registration
- Initialisation status
- Application lifecycle management
- Controlled application restart
- Critical-application monitoring support
- Processor-reset requests
- Shutdown requests
- Critical Data Store access, where used
- System and application status reporting

Executive Services should not contain all Mode Manager or FDIR policy. Instead:

- ES provides mechanisms such as application status, restart and processor reset.
- Health Monitoring and FDIR decide when recovery is required.
- The Mode Manager authorises spacecraft-level state transitions.

A representative startup sequence is:

```text
Bootloader selects image
→ FreeRTOS and BSP start
→ OSAL and PSP initialise
→ cFE core services start
→ Communication and storage services start
→ Mode Manager and Health Monitor start
→ Subsystem interfaces start
→ AOCS and propulsion applications start
→ Payload and background applications start
```

Each application should report whether initialisation succeeded. A failed return value from a critical startup stage should generate an event and a defined recovery action rather than leaving the system in a partially initialised state.

NASA's cFS Health and Safety application is a useful reference for application monitoring, event monitoring, watchdog servicing and execution-counter reporting. The proposed mission may reuse it, tailor it or implement a smaller equivalent application.
