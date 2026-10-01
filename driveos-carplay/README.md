# DriveOS CarPlay Navigation

Native iPhone + CarPlay navigation prototype designed for the vehicle's built-in CarPlay display.

## What it does

- Native CarPlay navigation scene
- Vehicle-display map using MapKit
- 3D/pitched map rendering
- GPS location tracking
- Destination search through CarPlay
- Driving route calculation
- Up to three route choices
- Route preview and ETA
- Turn-by-turn CarPlay navigation session
- Recenter control
- Separate phone companion screen

## Required before a real-car install

Apple requires the **CarPlay Navigation** entitlement:

`com.apple.developer.carplay-maps`

The entitlement must be approved for the Apple Developer account/App ID and included in the signing profile. The source file is included here, but simply adding the plist key does not grant the entitlement.

## Generate the Xcode project

This repo uses XcodeGen:

```bash
brew install xcodegen
cd driveos-carplay
xcodegen generate
open DriveOS.xcodeproj
```

In Xcode:

1. Select the DriveOS target.
2. Set your Apple Developer Team under Signing & Capabilities.
3. Change the bundle identifier if needed.
4. Ensure the approved CarPlay Navigation capability is attached to the App ID/profile.
5. Run on an iPhone or use the CarPlay Simulator.

## CarPlay Simulator

Run the iPhone app in Simulator, then choose:

**I/O → External Displays → CarPlay**

## Vehicle display

Once properly signed with the navigation entitlement, connecting the iPhone to a compatible CarPlay vehicle makes DriveOS available from the CarPlay app launcher.

## Design limitation

The navigation map itself can be custom-rendered. CarPlay controls, search, trip preview, buttons and turn guidance must use Apple's CarPlay framework/templates. This is required for apps shown while driving.
