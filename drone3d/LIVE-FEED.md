# DroneAir 3D Live Feed

DroneAir 3D can display demo traffic immediately. For real drone traffic, connect it to a backend/receiver that exposes decoded telemetry as HTTPS JSON or a secure WebSocket.

## Accepted JSON

Single object:

```json
{
  "id": "1581F...",
  "name": "Inspection Drone",
  "lat": 35.9912,
  "lon": -78.9043,
  "altitude": 82.0,
  "speed": 8.0,
  "heading": 217,
  "rssi": -61,
  "source": "Remote ID"
}
```

Or an array / wrapper:

```json
{"drones":[ ... ]}
```

OpenDroneID-style objects are also recognized:

```json
{
  "src":"ble",
  "rssi":-61,
  "basic_id":[{"uas_id":"1581F..."}],
  "loc":{
    "lat":35.9912,
    "lon":-78.9043,
    "alt_geo":82.0,
    "speed":8.0,
    "direction":217
  }
}
```

## Feed choices

- **HTTPS JSON polling**: endpoint returns current contacts every request.
- **WSS WebSocket**: send one JSON contact, an array, or a `{"drones":[]}` object per message.

## Remote ID receivers

FAA Remote ID is broadcast over radio (commonly Wi-Fi/Bluetooth). A practical full-band receiver can be built around an ESP32/Linux/OpenDroneID receiver and then bridged to HTTPS/WSS. iPhone/web browser radio access is limited, so this PWA is intentionally feed-driven rather than claiming it can directly receive every nearby Remote ID transmission.

## MAVLink

A MAVLink gateway can map vehicle telemetry to the simple fields above. Typical mappings:

- vehicle ID -> `id`
- GLOBAL_POSITION_INT latitude/longitude -> `lat`, `lon`
- relative/AMSL altitude -> `altitude`
- groundspeed -> `speed`
- heading -> `heading`

Keep any feed endpoint authenticated if it contains private fleet telemetry.
