#!/bin/bash
# Exit immediately if a command exits with a non-zero status.
set -e

# Define remote host and directory for clarity
REMOTE_USER="tsunami"
REMOTE_HOST="raid"
REMOTE_DIR="/home/user/tsunami-agent-plugins/"
REMOTE_SSH_TARGET="${REMOTE_USER}@${REMOTE_HOST}"

# Determine the next index for the archive folder
LAST_INDEX=$(ls -d plugin-archive/* 2>/dev/null | grep -oP '\d+' | sort -nr | head -n 1)
NEXT_INDEX=0
if [ -n "$LAST_INDEX" ]; then
  NEXT_INDEX=$((LAST_INDEX + 1))
fi

ARCHIVE_DIR="plugin-archive/${NEXT_INDEX}"
mkdir -p "${ARCHIVE_DIR}"

# Sync files from the remote server
# -a: archive mode
# -v: verbose
# -z: compress file data during the transfer
echo ">>> Syncing files from ${REMOTE_SSH_TARGET}:${REMOTE_DIR} to ${ARCHIVE_DIR}..."
rsync -avz "${REMOTE_SSH_TARGET}:${REMOTE_DIR}" "${ARCHIVE_DIR}"

echo ">>> Done!"