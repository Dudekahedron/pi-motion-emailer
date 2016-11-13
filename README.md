# pi-motion-emailer
RPi detections motion, sends timestamped image via email

This script watches a directory for new images (or videos) provided by motion events.
It then forwards those images (or videos) to a specified email address.

If no new images (or videos) are found, the script loops until one is found.
