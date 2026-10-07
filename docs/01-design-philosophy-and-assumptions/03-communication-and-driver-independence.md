### 1.3 Communication and Driver Independence

Mission applications and reusable libraries should not depend directly on low-level communication protocols, hardware abstraction layers or operating-system calls.

For example, the Propulsion Application should not open a UART or call a CSP transaction directly. It should publish a normalised command through the Software Bus // use a stable subsystem API 

A representative mission-facing call is:

```c
propulsion_status_t propulsion_command_send(
    const propulsion_command_t *command);
```

The implementation below this API may use any communication stack that is implemented for it.


The separation is:

```text
Mission Application
        ↓
cFE Software Bus message
        ↓
Subsystem Interface Application
        ↓
Subsystem-specific API
        ↓
Protocol encoder / decoder
        ↓
Generic transport interface
        ↓
Platform-specific driver
```

This is important because the Software Bus and the driver abstraction solve different problems:

- The **Software Bus** decouples independently scheduled flight applications.
- The **subsystem library** hides the device command and telemetry protocol.
- The **transport interface** hides whether the protocol uses UART, CAN, CSP, SpaceWire or another transport.
- The **platform driver** hides the operating system and peripheral implementation.

The same mission application can therefore run in a host simulation, on development hardware and on the final flight processor. It also becomes possible to replace a subsystem bus without rewriting the complete mission architecture.

The complete Software Bus and driver path is described in Sections 2.5 and 3.13.
