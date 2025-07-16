#!/bin/bash
# Exit immediately if a command exits with a non-zero status.
set -e

# Define remote host and directory for clarity
REMOTE_USER="tsunami"
REMOTE_HOST="raid"
REMOTE_DIR="/home/user/"
REMOTE_SSH_TARGET="${REMOTE_USER}@${REMOTE_HOST}"

# Sync files to the remote server
# -a: archive mode
# -v: verbose
# -z: compress file data during the transfer
# --exclude-from: read exclude patterns from file
echo ">>> Syncing files to ${REMOTE_SSH_TARGET}:${REMOTE_DIR}..."
rsync -avz --exclude-from=.syncignore . "${REMOTE_SSH_TARGET}:${REMOTE_DIR}"

# Execute the installation command on the remote server
echo ">>> Installing package on remote server..."
ssh "${REMOTE_SSH_TARGET}" "cd ${REMOTE_DIR} && python3 -m pip install . --break-system-packages"

echo ">>> Done!"