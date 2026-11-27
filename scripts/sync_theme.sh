#!/bin/sh
# Copy the shared tiedy theme (../tamondigital.github.io/theme/) into this app: CSS beside the app's styles, the
# script under public/. The copies are committed so a build never needs the theme repo; edit the theme there.
set -e
SRC="$(dirname "$0")/../../tamondigital.github.io/theme"
DIR="$(dirname "$0")/.."
cp "$SRC/tokens.css" "$SRC/chrome.css" "$DIR/src/styles/theme/"
cp "$SRC/chrome.js" "$DIR/public/theme/"
echo "theme synced from $SRC"
