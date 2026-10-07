### 3.7 Command Ingest

Command Ingest receives telecommands from the communication layer and converts them into normalised Software Bus commands.

Its responsibilities include:

- Receiving a decoded frame or packet from the link layer
- Validating packet length and structure
- Checking command service and subtype
- Translating the packet into an internal command
- Publishing the command on the Software Bus
- Generating command acceptance reports

CRC, RDP and link-level retransmission are normally responsibilities of the underlying link or transport layer. Command Ingest may verify an end-to-end packet CRC if the selected packet format includes one, but it should not duplicate every lower-layer protocol mechanism.

Parameter checking is divided into two levels:

- Command Ingest checks common structural limits, lengths and encoding.
- The destination application checks mission semantics and current-state constraints.

For example, Command Ingest can verify that a propulsion duration is correctly encoded and within the representable field range. The Propulsion Application and Mode Manager decide whether that duration is allowed in the current mode, thermal state and propulsion state.

For example, something convoluted that can be done : the ground interface is PUS-compatible. CSP may be used as an onboard transport.

```text
Ground command
→ UHF or S-band link
→ Link and transport validation
→ PUS-compatible decoding
→ Command Ingest
→ Software Bus command
→ Destination CSP application
```

File transfer can be handled by a dedicated transfer application rather than making the normal command parser process large binary transfers. This keeps ordinary commanding small and predictable. CFDP in cFS provides something like that.
