#!/bin/bash

# macOS bash script to create .dmg installer

APP_NAME="Mouse Wiggler"
DMG_NAME="$APP_NAME.dmg"

# Create .dmg installer
hdiutil create -volname "$APP_NAME" -srcfolder . -ov -format UDZO "$DMG_NAME"