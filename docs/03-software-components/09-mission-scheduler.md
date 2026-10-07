### 3.9 Mission Scheduler

The Mission Scheduler manages planned and time-tagged operations.

It supports:

- Absolute time-tagged commands
- Relative sequences
- Periodic operations
- Deferred commands
- "maybe" conditional requests

The scheduler does not execute the complete operation inside its own task. It publishes a Software Bus command to the destination application, and that application performs the operation asynchronously.

```text
Scheduled time reached
→ Scheduler publishes command
→ Destination application validates current state, in case it cant start.
→ Application starts operation, tells scheduler when finished and return code.
```

Brief mission sequencing may be represented in the scheduler, but FDIR recovery policy and spacecraft-level transitions remain under the Health Monitor, FDIR and Mode Manager.

NASA's Stored Command application is an existing example of absolute and relative time-tagged command sequences. 

uPython is also used in some ESA missions, but I don't know how big of a problem is to implement.
