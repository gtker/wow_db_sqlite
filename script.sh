#! /usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

archive () {
    local archive="$1"
    shift
    touch -d 1970-01-01T00:00:00Z "$@"
    TZ=UTC zip -r -oX - "$@" > "$archive"
}


function download_and_zip_data()
{
    local VERSION="$1"

    wget -O "${VERSION}"-world-db.zip "https://github.com/cmangos/${VERSION}-db/releases/download/latest/${VERSION}-world-db.zip"

    unzip "${VERSION}-world-db.zip"
    rm "${VERSION}-world-db.zip"

    ./mysql2sqlite/mysql2sqlite "${VERSION}mangos.sql" | sqlite3 "${VERSION}.sqlite"
    sqlite3 "${VERSION}.sqlite" VACUUM

    rm "${VERSION}mangos.sql"

    rm "${VERSION}.zip" || true
    archive "${VERSION}.zip" "${VERSION}.sqlite"
    rm "${VERSION}.sqlite"
}

git submodule update --init --recursive

download_and_zip_data "classic"
download_and_zip_data "tbc"
download_and_zip_data "wotlk"
