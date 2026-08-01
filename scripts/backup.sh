#!/usr/bin/env sh
set -eu
mkdir -p backups
DB_PATH="${DATABASE_PATH:-./data/students.db}"
test -f "$DB_PATH" || { echo "Database not found: $DB_PATH"; exit 1; }
cp "$DB_PATH" "backups/students-$(date +%Y%m%d-%H%M%S).db"
echo "Backup created."
