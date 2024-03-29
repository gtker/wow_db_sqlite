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

        extract_sqlites(sqlite_file, expac)

        os.remove(sqlite_file)


def extract_sqlites(sqlite_file: str, expac: str):
    def run_sqlite(file:str, query: str):
        subprocess.run(["sqlite3", sqlite_file, '.headers on', '.separator "\n"', '.mode csv', f'.once {expac}/{file}.csv', query])

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
    run_sqlite("items", "SELECT * FROM item_template ORDER BY entry;")
    if expac == "wrath":
        run_sqlite("spells", "SELECT printf('%d', SpellFamilyFlags) as SpellFamilyFlags,Id,Category,Dispel,Mechanic,Attributes,AttributesEx,AttributesEx2,AttributesEx3,AttributesEx4,AttributesEx5,AttributesEx6,AttributesEx7,Stances,Stances2,StancesNot,StancesNot2,Targets,TargetCreatureType,RequiresSpellFocus,FacingCasterFlags,CasterAuraState,TargetAuraState,CasterAuraStateNot,TargetAuraStateNot,CasterAuraSpell,TargetAuraSpell,ExcludeCasterAuraSpell,ExcludeTargetAuraSpell,CastingTimeIndex,RecoveryTime,CategoryRecoveryTime,InterruptFlags,AuraInterruptFlags,ChannelInterruptFlags,ProcFlags,ProcChance,ProcCharges,MaxLevel,BaseLevel,SpellLevel,DurationIndex,PowerType,ManaCost,ManaCostPerlevel,ManaPerSecond,ManaPerSecondPerLevel,RangeIndex,Speed,ModalNextSpell,StackAmount,Totem1,Totem2,Reagent1,Reagent2,Reagent3,Reagent4,Reagent5,Reagent6,Reagent7,Reagent8,ReagentCount1,ReagentCount2,ReagentCount3,ReagentCount4,ReagentCount5,ReagentCount6,ReagentCount7,ReagentCount8,EquippedItemClass,EquippedItemSubClassMask,EquippedItemInventoryTypeMask,Effect1,Effect2,Effect3,EffectDieSides1,EffectDieSides2,EffectDieSides3,EffectRealPointsPerLevel1,EffectRealPointsPerLevel2,EffectRealPointsPerLevel3,EffectBasePoints1,EffectBasePoints2,EffectBasePoints3,EffectMechanic1,EffectMechanic2,EffectMechanic3,EffectImplicitTargetA1,EffectImplicitTargetA2,EffectImplicitTargetA3,EffectImplicitTargetB1,EffectImplicitTargetB2,EffectImplicitTargetB3,EffectRadiusIndex1,EffectRadiusIndex2,EffectRadiusIndex3,EffectApplyAuraName1,EffectApplyAuraName2,EffectApplyAuraName3,EffectAmplitude1,EffectAmplitude2,EffectAmplitude3,EffectMultipleValue1,EffectMultipleValue2,EffectMultipleValue3,EffectChainTarget1,EffectChainTarget2,EffectChainTarget3,EffectItemType1,EffectItemType2,EffectItemType3,EffectMiscValue1,EffectMiscValue2,EffectMiscValue3,EffectMiscValueB1,EffectMiscValueB2,EffectMiscValueB3,EffectTriggerSpell1,EffectTriggerSpell2,EffectTriggerSpell3,EffectPointsPerComboPoint1,EffectPointsPerComboPoint2,EffectPointsPerComboPoint3,EffectSpellClassMask1_1,EffectSpellClassMask1_2,EffectSpellClassMask1_3,EffectSpellClassMask2_1,EffectSpellClassMask2_2,EffectSpellClassMask2_3,EffectSpellClassMask3_1,EffectSpellClassMask3_2,EffectSpellClassMask3_3,SpellVisual,SpellVisual2,SpellIconID,ActiveIconID,SpellPriority,SpellName,SpellName2,SpellName3,SpellName4,SpellName5,SpellName6,SpellName7,SpellName8,SpellName9,SpellName10,SpellName11,SpellName12,SpellName13,SpellName14,SpellName15,SpellName16,Rank1,Rank2,Rank3,Rank4,Rank5,Rank6,Rank7,Rank8,Rank9,Rank10,Rank11,Rank12,Rank13,Rank14,Rank15,Rank16,ManaCostPercentage,StartRecoveryCategory,StartRecoveryTime,MaxTargetLevel,SpellFamilyName,SpellFamilyFlags2,MaxAffectedTargets,DmgClass,PreventionType,StanceBarOrder,DmgMultiplier1,DmgMultiplier2,DmgMultiplier3,MinFactionId,MinReputation,RequiredAuraVision,TotemCategory1,TotemCategory2,AreaId,SchoolMask,RuneCostID,SpellMissileID,PowerDisplayId,EffectBonusCoefficient1,EffectBonusCoefficient2,EffectBonusCoefficient3,EffectBonusCoefficientFromAP1,EffectBonusCoefficientFromAP2,EffectBonusCoefficientFromAP3,SpellDescriptionVariableID,SpellDifficultyId,IsServerSide,AttributesServerside FROM spell_template ORDER BY id;")
    else:
        run_sqlite("spells", "select * from spell_template ORDER BY id;")

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

