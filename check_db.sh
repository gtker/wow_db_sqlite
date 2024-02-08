#!/usr/bin/env bash

set -e
set -u
set -o pipefail
set -x

CARGO_COMMAND="/home/user/.cargo/bin/cargo"

if ! command -v "$CARGO_COMMAND" &> /dev/null
then
    echo "Unable to find '$CARGO_COMMAND' command."
    exit 1
fi

if ! command -v git &> /dev/null
then
    echo "Unable to find 'git' command."
    exit 1
fi

echo "Running as $(whoami)"

SQLITES_GIT='github-as-gtker:gtker/wow_db_sqlite.git'
MESSAGES_GIT='github-as-gtker:gtker/wow_messages.git'

SQLITES="/home/user/cache/wow_db_sqlite"
MESSAGES="/home/user/cache/wow_messages"

if [ ! -d "$SQLITES" ]; then
    git clone --depth 1 "$SQLITES_GIT" "$SQLITES"
    git clone --depth 1 "$MESSAGES_GIT" "$MESSAGES"

    cd "$SQLITES"
    git submodule update --init --recursive
fi

cd "$MESSAGES"
git fetch origin
git reset --hard origin/main

cd "$SQLITES"
git fetch origin
git reset --hard origin/main

"$SQLITES/update.py"


cd "$MESSAGES"

$CARGO_COMMAND ramdisk unmount || true
$CARGO_COMMAND ramdisk mount

CARGO_INCREMENTAL=0 WOWM_SQLITE_DB_PATH="$SQLITES" "$CARGO_COMMAND" gen && "$CARGO_COMMAND" test --all-features -j 1 --no-run && "$CARGO_COMMAND" test --all-features

$CARGO_COMMAND ramdisk unmount

if [[ $(git status --porcelain | wc -l) -ne "0" ]]; then
    DIFF="$(git diff --stat HEAD)"
    git diff --stat HEAD

    cd "$MESSAGES"
    git commit --all --message "Auto update wow_db_sqlite version"
    git push

    cd "$SQLITES"
    git commit --all --message "Auto update version"
    git push

    /usr/local/bin/send-email "wow_messages auto updated" "The wow_messages and wow_db_sqlite repos have been updated.\n\n${DIFF}"
fi


