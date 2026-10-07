## 4. Scheduling and Real-Time Behaviour

The software runs on a single-core processor using the FreeRTOS fixed-priority, pre-emptive scheduler.

Task priorities are assigned according to timing criticality. A high-level functional importance does not automatically mean a high RTOS priority; priority is based on the required response time, deadline and possible consequence of delayed execution.

The proposed priority groups are:

| Priority group | Main functions |
|---|---|
| Critical | Emergency inhibits, watchdog coordination and time-critical hardware actions |
| Very high | Sensor acquisition, AOCS model execution and actuator output |
| High | Propulsion sequencing and propulsion-state monitoring |
| Medium-high | Health monitoring, Command Ingest and Mode Manager |
| Medium | Mission Scheduler, housekeeping generation and subsystem coordination |
| Low | File management, payload buffering and downlink preparation |
| Background | Software upload, log processing, checksums and diagnostics |

The exact task periods depend on the final AOCS and propulsion requirements. Initial values can be assigned during prototyping and replaced with measured values after target-hardware profiling.

| Task                 | Initial scheduling approach                           |
| -------------------- | ----------------------------------------------------- |
| Sensor acquisition   | Fixed-rate periodic task                              |
| AOCS model runner    | Fixed-rate periodic task                              |
| Actuator output      | Fixed-rate periodic or synchronised with AOCS         |
| Propulsion sequencer | Event-driven state machine with timed transitions     |
| Health monitoring    | Multi-rate periodic monitoring                        |
| Command Ingest       | Event-driven with bounded processing                  |
| Mission Scheduler    | Periodic release of stored or time-tagged commands    |
| Housekeeping         | Low-rate periodic task                                |
| Software update      | Background task, suspended during critical operations |

Periodic tasks should use absolute releases, for example `vTaskDelayUntil()`, rather than delaying relative to the end of the previous execution. This avoids accumulated timing drift.

```c
static void aocs_task(void *argument)
{
    TickType_t next_release = xTaskGetTickCount();

    for (;;)
    {
        aocs_execute_cycle();

        vTaskDelayUntil(
            &next_release,
            pdMS_TO_TICKS(AOCS_PERIOD_MS));
    }
}
```

Interrupt Service Routines should only perform the minimum required work:

- Capture a timestamp
- Read or clear hardware status
- Complete a DMA transaction
- Store received data in a bounded buffer
- Notify the corresponding task

Packet parsing, retries, model execution, file access and detailed event generation should be performed in task context.

The critical control path is:

```mermaid
flowchart LR
    TIMER["Periodic Release"]
    SENSOR["Sensor Acquisition"]
    VALIDATE["Validate and Timestamp"]
    AOCS["AOCS Model Step"]
    LIMIT["Limits and Inhibits"]
    OUTPUT["Actuator Command"]
    MONITOR["Deadline Monitoring"]

    TIMER --> SENSOR
    SENSOR --> VALIDATE
    VALIDATE --> AOCS
    AOCS --> LIMIT
    LIMIT --> OUTPUT
    OUTPUT --> MONITOR
```

Critical tasks shall have:

- A defined period and deadline
- A bounded input queue
- A measured execution time
- A monitored stack allocation
- A defined response to a missed deadline
- No unbounded file or communication operations

The cFE Software Bus pipes are sized according to the expected message rate and worst-case consumer latency. Critical traffic should use dedicated pipes and appropriately prioritized consumer tasks rather than assuming that one message can overtake another inside the same FIFO pipe.


The target is to keep nominal CPU utilization below approximately 45%, with planned worst-case utilization below 60%. These are initial design targets rather than fixed requirements and must be confirmed through measurement on the final OBC.

---
