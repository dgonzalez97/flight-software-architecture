### 3.4 Time Services

Time Services provide consistent time information to the applications.

The architecture distinguishes between:

- **Monotonic execution time**, derived from a stable hardware timer and used for control-loop periods, timeouts.
- **Mission elapsed time**, used for spacecraft-relative operations (i.e in 5000ms)
- **Spacecraft absolute time**, correlated with UTC or TAI through ground, GNSS, an RTC or another external source (API uses time.h)
- **Time quality**, indicating whether the current absolute time is valid and how it was obtained. (some apps/cmds may need better quality)

Time Services are responsible for:

- Time correlation
- Spacecraft-time distribution
- Timestamp generation
- Time-quality reporting
- External time synchronisation
- PPS handling or distribution, where implemented in software
- Support for time-tagged operations

Control loops use monotonic time. Ground-correlated absolute time is used for operations, telemetry and scheduling.

A change in absolute spacecraft time must not disturb periodic task execution. For example, correcting UTC by several seconds must not cause the AOCS task to execute twice or skip a control cycle.

The hardware PLL may be part of the clock-generation or clock-discipline implementation, but it is not itself the software time source. 
The software time source is the selected hardware timer, counter, RTC or external timing input exposed through the PSP and Time Services.
