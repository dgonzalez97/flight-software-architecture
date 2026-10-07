### 2.3 FreeRTOS Adaptation of cFE

The cFS architecture separates operating-system-specific functionality through OSAL and platform-specific functionality through the PSP.

For this mission, the intention is not to port every cFS application.

The OSAL implementation provides the FreeRTOS mechanisms required by these services. The PSP provides the processor- and board-specific functions, including:

- Early hardware initialisation
- Reset-reason access
- Watchdog control
- Non-volatile boot metadata
- Processor exceptions
- Hardware timers
- Memory-map definitions
- Board-specific startup logic

The preferred approach is:

1. Start from the published cFE, OSAL and PSP interfaces.
2. Identify the exact services required by the mission.
3. Implement and verify the required FreeRTOS OSAL backend.
4. Implement the processor- and board-specific PSP.
5. Avoid modifying cFE core behaviour unless a requirement makes it necessary.
6. Measure CPU, RAM, stack, queue and storage use on the target hardware.
7. Use the cFS Test Framework,

https://www.mdpi.com/2079-9292/15/5/1020 

This paper goes insight of the cFS port into FreeRTOS.
