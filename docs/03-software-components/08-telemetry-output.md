### 3.8 Telemetry Output

Telemetry Output subscribes to configured Software Bus messages and prepares them for ground transmission.

Its responsibilities include:

- Subscribing to selected internal telemetry
- Adding timestamps and sequence counters
- PUS-compatible packetisation
- Selecting or requesting the appropriate ground link
- Applying rate and priority configuration
- Sending command-verification reports
- Separating critical telemetry from bulk data

Representative telemetry classes are:

| Class | Examples | Preferred handling |
|---|---|---|
| Critical | Safe-mode state, propulsion fault, boot failure | UHF, highest priority |
| High | Command verification, AOCS state, power status | UHF or configured nominal link |
| Normal | Housekeeping and subsystem telemetry | Scheduled nominal downlink |
| Bulk | Payload files, detailed logs, memory dumps | S-band or other high-rate link |

UHF is assumed to remain available for nominal commanding, housekeeping and contingency recovery. S-band is preferred for payload data, detailed logs and large software-image transfers.

Telemetry Output should not block critical applications while waiting for a radio. Applications publish messages and continue; the communications services manage bounded queues, link availability and drop policies.
