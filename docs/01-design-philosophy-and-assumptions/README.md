## 1. Design Philosophy and Assumptions

Keeping in mind the expected functions of this OBC, especially real-time AOCS control and propulsion supervision, the system needs a deterministic execution model. For that reason, the baseline proposed here is a hard real-time, single-core architecture running FreeRTOS.

The single-core decision is mainly driven by the size of the team, the fixed launch schedule and the advantages of having an architecture that is easier to understand, profile and verify. The complete critical workload should be schedulable on one core without relying on parallel execution.

FreeRTOS is selected because it is lightweight, open source and familiar to many software developers. Its default single-core scheduler is fixed-priority and preemptive: the highest-priority ready task executes, while lower-priority work can run when critical tasks are blocked waiting for their next release or for an event.

Other operating systems remain technically possible:

- **RTEMS** has strong space heritage and is a valid alternative, but it generally requires a larger integration and configuration effort than the small FreeRTOS baseline proposed here.
- **VxWorks** is also suitable for critical embedded systems and can provide commercial support and qualification material, but licensing cost and team experience would need to justify its use.
- **ChibiOS** is a compact RTOS that could support a smaller embedded platform, although FreeRTOS is preferred because it is more familiar to the proposed team.
- **Linux with PREEMPT_RT** could be considered if the platform later required complex networking, large filesystems or payload-processing frameworks. It is not selected for the primary control processor because the AOCS and propulsion paths benefit from a smaller and more predictable runtime environment.

Regardless of the selected RTOS, the mission applications should not call the native operating-system API directly. The platform will be built over a small **Operating System Abstraction Layer**, or OSAL, which provides only the services required by the flight software:

- Tasks
- Queues
- Mutexes
- Binary and counting semaphores
- Task notifications / Software ISR
- Software timers
- Monotonic time


This does not make a future RTOS replacement automatic. A change of RTOS would still require timing analysis, driver adaptation and revalidation. However, it prevents operating-system-specific calls from spreading through the mission applications and keeps the changes concentrated in the OSAL, Platform Support Package and low-level drivers.

<!-- nav:start -->

- [1.1 FreeRTOS](01-freertos.md)
- [1.2 Propulsion](02-propulsion.md)
- [1.3 Communication and Driver Independence](03-communication-and-driver-independence.md)
- [1.4 Boot and OTA Firmware Update as Core Architecture](04-boot-and-ota-firmware-update-as-core-architecture.md)

<!-- nav:end -->
