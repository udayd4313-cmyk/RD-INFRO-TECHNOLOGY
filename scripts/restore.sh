#!/usr/bin/env sh
set -eu
BACKUP="${1:?Usage: ./scripts/restore.sh backups/file.db}"
DB_PATH="${DATABASE_PATH:-./data/students.db}"
mkdir -p "$(dirname "$DB_PATH")"
cp "$BACKUP" "$DB_PATH"
echo "Database restored from $BACKUP"
