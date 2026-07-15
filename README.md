# scent-max

A replacement app for a Bluetooth-connected "Scent Life" scent diffuser,
since the official iOS app is unreliable. This is a two-phase project:

1. **Reverse-engineer the BLE protocol** the diffuser speaks (no public docs
   exist for it).
2. **Build a real control app** once the protocol is known.

## Phase 1: BLE Explorer (protocol discovery tool)

`index.html` is a single-file Web Bluetooth GATT explorer. It scans for BLE
devices, connects, lists every service and characteristic, and lets you
read / subscribe to notifications / write raw hex — everything needed to
reverse-engineer the diffuser's command set.

**Live tool:** https://dcglobalsolutions90-code.github.io/scent-max/

### Requirements

- **Bluefy** on iOS (App Store) — Safari does not support Web Bluetooth at
  all. Open the GitHub Pages URL above inside Bluefy.
- Or desktop/Android Chrome, for testing without the physical device present.
- The page must be served over HTTPS (GitHub Pages satisfies this); Bluefy
  will not open local files directly.

### One-time repo setup for GitHub Pages

If the live URL above isn't serving yet, enable Pages once in the repo:
**Settings → Pages → Build and deployment → Source: Deploy from a branch →
Branch: `main` / root.** `index.html` is already at the repo root, so no
further build step is required — it's a static file.

### Using the explorer against the diffuser

1. Put the diffuser in range and make sure the official Scent Life app is
   **not** currently connected to it (only one BLE central can hold the
   connection at a time).
2. Open the explorer in Bluefy, tap **Scan & Connect**, and pick the
   diffuser from the device picker.
3. Expand each service and note anything with `notify`/`indicate` — tap
   **Subscribe** on those first.
4. To passively capture the real protocol: leave the explorer subscribed,
   then operate the diffuser from the *official* app on a second phone and
   watch the log panel for incoming notification bytes.
5. To actively probe: try writing simple values (`00`, `01`, `FF`,
   incrementing levels) to `write`/`writeWithoutResponse` characteristics
   and watch what the machine physically does.
6. Use **Export .json** in the log panel to save a session for later
   analysis, and transcribe confirmed findings into [`PROTOCOL.md`](PROTOCOL.md).

If a service doesn't show up after connecting, add its UUID to the "extra
optional service UUIDs" field before reconnecting — Web Bluetooth only
exposes services declared at request time. See [`docs/hci-capture.md`](docs/hci-capture.md)
for how to get an exact command list via a Bluetooth HCI packet capture
instead of trial-and-error, which is the most reliable route if a Mac is
available.

## Deliverable: [`PROTOCOL.md`](PROTOCOL.md)

The protocol spec — service/characteristic UUIDs and byte-level command
format — gets filled in here as it's discovered. Phase 2 (the real control
app) depends on this being populated first.

## Phase 2: control app (not started)

Once `PROTOCOL.md` is filled in, the plan is to extend `index.html` (or
build a native SwiftUI + CoreBluetooth app if a Mac is available) into a
proper control UI: power toggle, intensity slider/presets, and a
timer/schedule control, with last-used settings persisted locally.
