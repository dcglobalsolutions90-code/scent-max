# Capturing a Bluetooth HCI snoop log from iOS

This is the most reliable way to extract the exact GATT writes the real
Scent Life app sends, without any guessing.

## Option A: on-device developer log (no Mac required for capture, but you
need a Mac to open the result in Wireshark)

1. On iPhone: Settings → Privacy & Security → Analytics & Improvements →
   Analytics Data → (in newer iOS versions, use the dedicated Bluetooth
   toggle instead, see Option B) — this path varies by iOS version.
2. Preferred modern path: install the **Additional Tools for Xcode**
   package on a Mac (Apple Developer downloads), which includes
   **PacketLogger**.

## Option B: Xcode PacketLogger (recommended, requires a Mac)

1. On the Mac, download "Additional Tools for Xcode" from
   https://developer.apple.com/download/all/ (search "Additional Tools").
2. Open `Hardware/PacketLogger.app` from the downloaded disk image.
3. Connect the iPhone to the Mac via USB/cable and trust it.
4. In PacketLogger, select the iPhone as the capture target and start
   logging.
5. On the iPhone, open the real Scent Life app, connect to the diffuser,
   and press through the actions you want captured one at a time (power on,
   wait, power off, set intensity to each level, set timer, etc). Narrate
   or note the wall-clock time of each button press so you can correlate it
   with the log afterward.
6. Stop the capture in PacketLogger and save it as a `.pklg` file.

## Reading the capture

1. In PacketLogger, filter for `ATT` (Attribute Protocol) packets — this is
   the layer GATT read/write/notify operations ride on.
2. Look for `Write Request` / `Write Command` packets sent from the phone
   to the peripheral — these are the app's commands. Note the attribute
   handle and value bytes.
3. Look for `Read Response` and `Handle Value Notification` packets — these
   are data coming back from the device (status/feedback).
4. Cross-reference attribute handles with the `Read By Group Type
   Response`/`Find Information Response` packets earlier in the capture
   (or with what `index.html` shows you) to map each handle back to a
   characteristic UUID.
5. Transcribe the findings into `PROTOCOL.md`.

## Alternative: Android HCI snoop log

If a Mac isn't available but an Android phone is, Android has a built-in
"Enable Bluetooth HCI snoop log" developer option that dumps a
`btsnoop_hci.log` file readable directly in Wireshark (no PacketLogger
needed) — but this only works if the Scent Life app also has an Android
build.
