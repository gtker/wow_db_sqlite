#!/usr/bin/env python3

import subprocess
import os
import zipfile
import urllib.request
import argparse

WOW_MESSAGES_REPO = "https://github.com/gtker/wow_messages/"
EXPANSIONS = [("classic", "vanilla"), ("tbc", "tbc"), ("wotlk", "wrath")]


def download_databases():
    for expansion, expac in EXPANSIONS:
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

        extract_sqlites(sqlite_file, expac)


def extract_sqlites(sqlite_file: str, expac: str):
    def run_sqlite(file:str, query: str):
        subprocess.run(["sqlite3", sqlite_file, '.headers on', '.mode csv', f'.once {expac}/{file}.csv', query])

    run_sqlite("pet_names", "SELECT * from pet_name_generation")
    run_sqlite("tavern_triggers", "SELECT * from areatrigger_tavern;")
    run_sqlite("quest_triggers", "SELECT * FROM areatrigger_involvedrelation;")
    run_sqlite("teleport_triggers", "SELECT * FROM areatrigger_teleport;")
    run_sqlite("actions", "SELECT * FROM playercreateinfo_action;")
    run_sqlite("distinct_actions", "SELECT DISTINCT race, class FROM playercreateinfo_action ORDER BY race, class;")
    run_sqlite("level_exp", "select lvl level, xp_for_next_level exp from player_xp_for_level ORDER BY level;")
    run_sqlite("exploration_exp", "select level, basexp exp from exploration_basexp where level != 0 ORDER BY level;")
    run_sqlite("stat_data", "SELECT race, l.class, l.level, str, agi, sta, inte, spi, basehp, basemana FROM player_levelstats l LEFT JOIN player_classlevelstats c on l.level = c.level and l.class = c.class;")
    run_sqlite("skills", "SELECT * FROM playercreateinfo_skills ORDER BY skill;")
    run_sqlite("initial_spells", "SELECT * FROM playercreateinfo_spell;")


def main():
    parser = argparse.ArgumentParser(prog='update.py')
    parser.add_argument('-x', '--extract-only', action='store_true', default=False)
    args = parser.parse_args()

    if args.extract_only:
        for expansion, expac in EXPANSIONS:
            extract_sqlites(f"{expansion}.sqlite", expac)
    else:
        download_databases()


if __name__ == '__main__':
    main()

