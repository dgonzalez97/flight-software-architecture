### 1.2 Propulsion

Two propulsion-control approaches have been considered.

The first approach is direct actuation from the OBC. In this architecture, the OBC controls valve timing, actuator sequencing and immediate shutdown.

The second approach uses a dedicated Propulsion Control Unit, or PCU/ECU, while the OBC sends high-level commands and supervises the operation.

The selected baseline is the second approach: the propulsion system provides its own dedicated control unit, and the OBC interfaces with it through a defined command-and-telemetry protocol.

This is the most suitable boundary when the propulsion unit is intended to operate as a standalone subsystem or product. It also provides better fault containment and separates mission-level autonomy from low-level actuator timing.

The propulsion control unit is responsible for:

- Low Level actuator (valves, heaters, sensors), and timing.
- Local watchdog supervision
- Fast actuator-level fault detection, immediate shutdown when required.
- Returning the propulsion system to a safe state if communication with the OBC is lost

The OBC is responsible for:

- Arming and disarming
- Mission-level sequencing
- Spacecraft-mode checks
- Inhibit management
- Command
- Telemetry assessment
- Fault reporting
- Recovery coordination
- Coordination with AOCS, thermal and power constraints

The interface between the OBC and the propulsion controller will use a command-and-telemetry protocol. Additional discrete signals may be used where appropriate, for example:

- PPS or synchronisation input
- Hardware inhibit
- Ready indication
- Safe-state indication
- Fault indication
- Emergency shutdown

The OBC commands propulsion operations according to the AOCS constraints, propulsion requirements, spacecraft modes and FDIR specification. Operations may originate from ground commands, the Mission Scheduler or authorised autonomous logic.

If direct control of the propulsion valves is required, the architecture can support it. However, the task controlling the valves would become one of the highest-criticality tasks in the OBC and would require:

- Dedicated hardware timers
- Strict worst-case execution-time analysis
- Independent watchdogs
- Direct actuator feedback (more cables, which are bad for low latency)
- Bounded interrupt latency
- Additional software and hardware safety barriers
- More extensive verification

For this reason, direct valve control is not selected as the baseline for this example.
