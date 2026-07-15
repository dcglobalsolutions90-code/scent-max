# Scent Life Diffuser — BLE Protocol Spec

Status: **not yet captured**. This document is the deliverable for Phase 1
(protocol discovery). Fill it in as you extract information using
`index.html` (the BLE explorer) and/or an HCI snoop log capture.

## Device identification

- Model / label name:
- FCC ID (from the device's regulatory label, if present):
- Chipset / module (if identifiable from FCC filing or teardown):
- Advertised BLE name (as seen in the scan picker):
- MAC / device identifier:

## GATT structure

For each service discovered, list its characteristics and properties.

### Service: `<uuid>` — `<human name if known>`

| Characteristic UUID | Properties | Purpose | Notes |
|---|---|---|---|
| `<uuid>` | read / write / writeWithoutResponse / notify / indicate | | |

Repeat this section per service.

## Command format

Document each control action as a concrete byte sequence written to a
specific characteristic. Capture these either by:
- writing candidate bytes via the explorer and observing the device, or
- reading them directly out of an HCI snoop log while operating the real
  Scent Life app (see `docs/hci-capture.md` for how to grab that log).

### Power on/off

- Target characteristic:
- Bytes for ON:
- Bytes for OFF:
- Confirmed via:

### Intensity / level

- Target characteristic:
- Byte encoding (e.g. single byte 0x01–0x05, or other scale):
- Confirmed levels:

### Timer / schedule

- Target characteristic:
- Byte encoding:
- Notes:

### Status / feedback (notify characteristics)

- Source characteristic:
- Byte layout of notifications:
- What triggers a notification:

## Open questions

- [ ] Does the device require a specific write order (e.g. handshake byte
      before commands are accepted)?
- [ ] Is there any authentication/pairing requirement beyond standard BLE
      pairing?
- [ ] Are there checksum/CRC bytes in the command frames?
