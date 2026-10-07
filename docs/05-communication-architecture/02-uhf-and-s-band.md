### 5.2 UHF and S-band

The architecture assumes two logical communication classes.

**UHF or equivalent low-rate link**

- Nominal telecommands
- Basic housekeeping
- Command verification
- Safe-mode telemetry
- Contingency access
- Recovery commands

**S-band or equivalent high-rate link**

- Payload files
- Detailed logs
- Memory dumps
- Software images
- Large table uploads
- Bulk engineering telemetry

The spacecraft must not depend on the high-rate link for basic recovery. A minimum command and telemetry capability should remain available through the low-rate link.

Bulk transfers are block-based, resumable and rate-limited. They execute at lower priority than AOCS, propulsion and critical telemetry.

Selected cFS applications can support this architecture, or custom ports of uFS, FTP, BTP, etc.

- HK for configurable housekeeping packets
- DS for storing selected Software Bus messages
- CFDP for file transfer and controll



---
