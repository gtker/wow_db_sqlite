#!/usr/bin/env python3

import subprocess
import os
import zipfile
import urllib.request

WOW_MESSAGES_REPO = "https://github.com/gtker/wow_messages/"
EXPANSIONS = ["classic", "tbc", "wotlk"]


def cleanup():
    for expansion in EXPANSIONS:
        for file in [f"{expansion}-sqlite-db.zip", f"{expansion}logs.sqlite", f"{expansion}mangos.sqlite", f"{expansion}realmd.sqlite", f"{expansion}characters.sqlite"]:
            if os.path.isfile(file):
                os.remove(file)


def download_databases():
    for expansion in EXPANSIONS:
        file_name = f"{expansion}-sqlite-db.zip"

        print(f"Downloading '{file_name}'")
        urllib.request.urlretrieve(f"https://github.com/cmangos/{expansion}-db/releases/download/latest/{file_name}", file_name)

        print(f"Extracting '{file_name}'")
        sqlite_file = f"{expansion}mangos.sqlite"
        with zipfile.ZipFile(file_name) as zip_ref:
            zip_ref.extract(sqlite_file)

        print(f"Removing '{file_name}'")
        os.remove(file_name)

        print(f"Renaming '{sqlite_file}' to '{expansion}.sqlite'")
        os.rename(sqlite_file, f"{expansion}.sqlite")


def main():
    download_databases()


if __name__ == '__main__':
    main()


