#!/bin/bash
# Serve the project management website locally
echo "Starting ProjectFlow local server on http://localhost:8000"
echo "Press Ctrl+C to stop."
python3 -m http.server 8000
