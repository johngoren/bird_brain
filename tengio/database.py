import sqlite3
import os.path
import sys
import csv

DATA_FOLDER = '../data/'
ASSET_FOLDER = '../app/src/main/assets/databases/'
APP_DB = sqlite3.connect('%sbird-guide.db' % ASSET_FOLDER)
FILTER_DB = sqlite3.connect('%sbird_guide_filter.db' % DATA_FOLDER)
COLLINS_DB = sqlite3.connect('%s/maps-collins/Filter/distribution-WP.sqlite' % DATA_FOLDER)
BTO_DB = sqlite3.connect('%s/maps-bto/BTOSearch.db' % DATA_FOLDER)
ENTITY_DB = sqlite3.connect('%sStrix_BIRDGUIDE.db' % DATA_FOLDER)

def get_id(reference):
    """Get id from entity table given a reference"""
    statement = 'select entity_id from strix_entities where entity_reference = \'%s\' limit 1'
    ENTITY_CURSOR.execute(statement % reference)
    return ENTITY_CURSOR.fetchone()[0]

def scores():
    """prepare scores table"""
    CURSOR.execute("DROP TABLE IF EXISTS Scores")
    CURSOR.execute("CREATE TABLE Scores(id INT, score INT, code TEXT, morph TEXT, taxcode TEXT)")
    FILTER_CURSOR.execute("""SELECT optionid, score, taxamorphs.TaxonCode, taxamorphs.Morph
        FROM scores LEFT JOIN taxamorphs ON taxamorphs.taxonmorphid = scores.taxonmorphid;""")
    insert_statement = "INSERT INTO Scores VALUES(%s, %s, %s, \"%s\", \'%s\')"
    for row in FILTER_CURSOR:
        eid = get_id(row[2])
        CURSOR.execute(insert_statement % (row[0], int(row[1]), eid, row[3], row[2]))

    APP_DB.commit()
    return

def similarities():
    """Prepare similarities table"""
    CURSOR.execute("DROP TABLE IF EXISTS Similarities")
    CURSOR.execute("""CREATE TABLE Similarities(id INT, morph TEXT, similarId INT,
        similarMorph TEXT, priority INT)""")
    with open('%sSimilar_species.csv' % DATA_FOLDER, 'rU') as csvfile:
        reader = csv.reader(csvfile, dialect=csv.excel_tab)
        next(reader)
        for row in reader:
            #[,,species.larus_argentatus,juvenile']
            parts = row[0].replace('adult,adult summer', 'adult').split(",")
            #special case species.phoenicopterus_roseus
            sid = get_id(parts[0])
            part = parts[1]
            print "================================"
            print row
            print parts
            insert_statement = "INSERT INTO Similarities VALUES(%s, \"%s\", %s, \"%s\", %s)"
            stm = insert_statement % (sid, part, get_id(parts[2]), parts[3], 1)
            print stm
            CURSOR.execute(stm)
            if parts[4]:
                print "-", sid, part, get_id(parts[4]), parts[5]
                CURSOR.execute(insert_statement % (sid, part, get_id(parts[4]), parts[5], 2))
            if len(parts) < 7:
                continue
            if parts[6]:
                print "-", sid, part, get_id(parts[6]), parts[7]
                CURSOR.execute(insert_statement % (sid, part, get_id(parts[6]), parts[7], 3))
            if len(parts) < 9:
                continue
            if parts[8]:
                print "-", sid, part, get_id(parts[8]), parts[9]
                CURSOR.execute(insert_statement % (sid, part, get_id(parts[8]), parts[9], 4))
    APP_DB.commit()
    return

def morphs():
    """Prepare morphs table"""
    CURSOR.execute("DROP TABLE IF EXISTS Morphs")
    CURSOR.execute("CREATE TABLE Morphs(id INT, morph TEXT)")
    FILTER_CURSOR.execute("select TaxonCode, Morph from TaxaMorphs;")
    for row in FILTER_CURSOR:
        sid = get_id(row[0])
        print sid, row[1]
        CURSOR.execute("INSERT INTO Morphs VALUES(%s, \"%s\")" % (sid, row[1]))
    APP_DB.commit()
    return

def collins_maps():
    """Prepare collins table"""
    CURSOR.execute("DROP TABLE IF EXISTS collins")
    CURSOR.execute("CREATE TABLE Collins(id INT, region INT, season INT)")
    COLLINS_CURSOR.execute("""
    select region_reference, season_id, species_reference 
    from presence left join species on species.id = presence.species_id
    left join regions on presence.region_id = regions.id;""")
    insert_statement = "INSERT INTO Collins VALUES(%s, %s, %s)"
    for row in COLLINS_CURSOR:
        CURSOR.execute(insert_statement % (get_id(row[2]), get_id(row[0]), row[1]))

    APP_DB.commit()
    return

def bto_maps():
    """Prepare bto table"""
    CURSOR.execute("DROP TABLE IF EXISTS bto")
    CURSOR.execute("CREATE TABLE Bto(id INT, region TEXT, season INT)")
    BTO_CURSOR.execute("""
    select reference, square, is_winter from presence 
    left join species on species.id = presence.species_id;""")
    insert_statement = "INSERT INTO Bto VALUES(%s, \"%s\", %s)"
    for row in BTO_CURSOR:
        CURSOR.execute(insert_statement % (get_id(row[0]), row[1], row[2]))

    APP_DB.commit()
    return


#######################
## Execution
#######################

FILTER_CURSOR = FILTER_DB.cursor()
ENTITY_CURSOR = ENTITY_DB.cursor()
COLLINS_CURSOR = COLLINS_DB.cursor()
BTO_CURSOR = BTO_DB.cursor()
CURSOR = APP_DB.cursor()

scores()
similarities()
morphs()
collins_maps()
bto_maps()

CURSOR.close()
ENTITY_CURSOR.close()
FILTER_CURSOR.close()
COLLINS_CURSOR.close()
BTO_CURSOR.close()
