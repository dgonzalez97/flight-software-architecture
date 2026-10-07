## 2. Architectural Approach

The architecture I am most comfortable with is divided into six logical layers:

1. **Mission applications**
2. **Common mission services and reusable libraries**
3. **cFE-based core**
4. **Subsystem, COTS-device and communication libraries**
5. **Operating-system and hardware abstraction layers**
6. **FreeRTOS, board-support software and hardware**

The intended dependency direction is mainly downward:

```text
Mission Applications
        ↓
Common Mission Services
        ↓
cFE-Based Core
        ↓
Subsystem and Communication Libraries
        ↓
OSAL / PSP / HAL
        ↓
FreeRTOS / BSP / Hardware
```

Mission applications should not directly access:

- Native FreeRTOS primitives
- Peripheral registers
- UART, CAN or any comm drivers
- PUS packet definitions
- Filesystem implementations
- COTS-specific packet formats

These dependencies are isolated behind stable APIs and Software Bus messages.

This allows mission logic to be developed and tested independently from the final hardware. It also makes it possible to replace a subsystem, communication bus or processor without redesigning the complete flight software.

<!-- nav:start -->

- [2.1 Layered Architecture](01-layered-architecture.md)
- [2.2 Core Framework — cFE](02-core-framework-cfe.md)
- [2.3 FreeRTOS Adaptation of cFE](03-freertos-adaptation-of-cfe.md)
- [2.4 Application Organisation](04-application-organisation.md)
- [2.5 Application and Data Flow](05-application-and-data-flow.md)
- [2.6 Software Bus and External Networks](06-software-bus-and-external-networks.md)

<!-- nav:end -->
