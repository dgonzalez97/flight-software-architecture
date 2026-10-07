### 1.1 FreeRTOS

FreeRTOS is selected because the system includes hard real-time functions, particularly AOCS execution and propulsion sequencing.

If the propulsion subsystem is going to be a standalone product with its own controller, it will internally handle low-level actuation and accept high-level commands, time-tagged operations or PPS synchronisation from the OBC. 

This reduces the low-level propulsion timing handled by the OBC, but the OBC must still provide deterministic command sequencing, supervision and recovery coordination.

The FreeRTOS scheduler will use a fixed-priority, pre-emptive configuration. This makes the execution model relatively simple and analysable:

- The highest-priority ready task executes.
- AOCS and propulsion-related tasks can pre-empt telemetry, storage and background processing.
- Each periodic task can have a defined release rate, deadline and maximum permitted execution time.
- Worst-case execution time can be measured on the target hardware.
- Stack use, queue use, task execution and deadline misses can be monitored.
- The behaviour can be analysed without depending on a complex general-purpose process scheduler.

The system is assumed to use one processor core with enough throughput for the full nominal workload and the required recovery margin.

A multicore CPU can provide more processing capacity, but it also introduces:

- Race conditions
- Synchronisation complexity
- More complex worst-case execution-time analysis
- Possible interference between critical and non-critical workloads

Multicore operation does not make timing analysis impossible, but it makes the analysis and verification significantly more difficult. If a multicore processor is eventually selected, the safety-critical control path should remain independently schedulable on one core. Additional cores could then be used for payload processing, data compression or other non-critical functions.

Timing measurements should be performed on the target processor. CI/CD can then be used to detect timing regressions by comparing execution-time measurements, stack high-water marks and hardware-in-the-loop results against established limits. The build server itself cannot prove the target WCET, but it can automatically reject changes that exceed previously defined timing or resource thresholds during target-based testing.

FreeRTOS+CLI can also be integrated as an optional diagnostic interface. It is a small command-interpreter. It can be connected to UART, USB, Ethernet or another test interface and used during development and AIT.

The CLI should not become a second uncontrolled command path. Safety-critical commands must pass through the same validation, mode checks and authorisation rules as commands received through the nominal TM/TC interface. The CLI is disabled in the flight configuration.
