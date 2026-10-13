#!/bin/sh
# Copy the shared renderer into every skill that renders files. Run after editing _shared/warmnode.py.
cd "$(dirname "$0")/.." || exit 1
for s in ig-carousel ig-reel ig-story; do mkdir -p "$s/scripts"; cp _shared/warmnode.py "$s/scripts/warmnode.py"; done
echo "synced"
