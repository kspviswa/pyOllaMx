#!/bin/sh
# Create a folder (named dmg) to prepare our DMG in (if it doesn't already exist).
mkdir -p dist/dmg
# Empty the dmg folder.
rm -r dist/dmg/*
# Copy the app bundle to the dmg folder.
cp -r "build/macos/pyollamx.app" dist/dmg
# If the DMG already exists, delete it.
test -f "dist/PyOllaMx.dmg" && rm "dist/PyOllaMx.dmg"
create-dmg \
  --volname "PyOllaMx" \
  --volicon "icon.icns" \
  --window-pos 200 120 \
  --window-size 600 300 \
  --icon-size 100 \
  --icon "PyOllaMx.app" 175 120 \
  --hide-extension "PyOllaMx.app" \
  --app-drop-link 425 120 \
  "dist/PyOllaMx.dmg" \
  "dist/dmg/"