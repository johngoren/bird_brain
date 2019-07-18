import shutil
import os
import sys
import os.path
import sqlite3
import nameutils

SONG_FOLDER = '../data/songs/'
ASSET_FOLDER = '../app/src/main/assets/songs/'
DATA_FOLDER = '../data'
APP_FOLDER = '../app'
VALUES_FOLDER = '%s/src/main/res/values' % APP_FOLDER
ENTITIES_DB = '%s/Strix_BIRDGUIDE.db' % DATA_FOLDER
LANGUAGES = [
    ['en', '%s/' % VALUES_FOLDER],
    ['de', '%s-de/' % VALUES_FOLDER],
    ['fr', '%s-fr/' % VALUES_FOLDER],
    ['nb', '%s-no/' % VALUES_FOLDER],
    ['sv', '%s-sv/' % VALUES_FOLDER]
]

def clean():
    """delete existing songs file"""
    for root, dirs, files in os.walk(ASSET_FOLDER):
        for f in files:
            if f != ".gitignore" and f != "README":
                os.remove('%s%s' % (ASSET_FOLDER, f))
    return

def songs():
    songs = os.listdir(SONG_FOLDER)
    con = sqlite3.connect(ENTITIES_DB)
    c = con.cursor()
    c.execute('select entity_id, entity_reference from strix_entities where entity_type = \"species.song\";')
    for row in c:
        sid = row[0]
        reference = row[1]
        if reference.endswith("wav") :
            reference = "%s.m4a" % reference
        
        source = "%s%s" % (SONG_FOLDER, reference)
        destination = "%s%s" % (ASSET_FOLDER, "%s.m4a" % sid)
        try:
            shutil.copy(source, destination)
            print "%s => %s" % (source, destination)
        except IOError:
            print "================================"
            print "Missing file!"
            print "%s => %s" % (source, destination)
            print "================================"
    return

def isInStringsFile(value, file_path):
    """Controls if value is in strings file"""
    strings_file = file(file_path)
    for line in strings_file:
        if value in line:
            return True
    print "String value for %s is missing" % (value)
    return False

def audioWrapString(prefix, r):
    content = "%s%s" % (prefix, r)
    contentCheck = "\"%s%s\"" % (prefix, r)
    if isInStringsFile(contentCheck, '%s/songs.xml' % VALUES_FOLDER):
        return "%s" % content
    return "nf"


def songsModel():
    songFile = open('%s/src/main/java/com/natureguides/birdguide/model/data/SongsDataModel.java' % APP_FOLDER, 'wb')
    content = "package com.natureguides.birdguide.model.data;\n\n"
    content += "// CHECKSTYLE SUPPRESS 20 LINES\n"
    content += "import static com.natureguides.birdguide.R.string.*;\n\n"
    content += "import static java.util.Arrays.asList;\n"
    content += "import java.util.List;\n\n"
    content += "import com.natureguides.birdguide.model.Song;\n"
    content += "import static com.natureguides.birdguide.model.Song.so;\n\n"
    content += "public final class SongsDataModel {\n"
    content += "public static final List<Song> SONGS = asList("
    con = sqlite3.connect(ENTITIES_DB)
    c = con.cursor()
    c.execute('select entity_id, parent_entity_id, entity_reference from strix_entities where entity_type = "species.song";')
    for row in c:
        sid = row[0]
        st = audioWrapString("st", sid)
        sl = audioWrapString("sl", sid)
        sa = audioWrapString("sa", sid)
        sm = audioWrapString("sm", sid)
        bsa = audioWrapString("bsa", sid)
        content += "so(%s,%s,%s,%s,%s,%s,%s)," % (sid, row[1], st, sl, sa, sm, bsa)

    content = content[:-1]
    content+=");\n}\n"
    songFile.write(content)
    return

def generateStringForSongs(language, directoryName):
    if not os.path.exists(directoryName):
        os.makedirs(directoryName)

    f1 = open("%ssongs.xml" % directoryName, 'wb')
    f1.write("<resources xmlns:tools=\"http://schemas.android.com/tools\" tools:ignore=\"all\">\n")
    if os.path.exists(DATA_FOLDER):
        con = sqlite3.connect(ENTITIES_DB)
        c = con.cursor()
        if language == "en":
            c.execute("""
            select strix_entities.entity_id, attribute_value, attribute_key
            from strix_entities
            left join strix_entity_attributes on strix_entity_attributes.entity_id = strix_entities.entity_id
            where strix_entities.entity_type = 'species.song'
            and attribute_key in ('SoundAuthor', 'SoundLocation', 'SoundMonth', 'SoundTitle', 'BackgroundSpeciesAudio')
            and ( attribute_language_code = '%s' or attribute_language_code = 'none');""" % language)
        else:
            c.execute("""
            select strix_entities.entity_id, attribute_value, attribute_key
            from strix_entities
            left join strix_entity_attributes on strix_entity_attributes.entity_id = strix_entities.entity_id
            where strix_entities.entity_type = 'species.song'
            and attribute_key in ('SoundAuthor', 'SoundLocation', 'SoundMonth', 'SoundTitle', 'BackgroundSpeciesAudio')
            and ( attribute_language_code = '%s');""" % language)
        for row in c:
            value = row[1].encode('utf-8').replace("&", "&amp;").replace("\'", "\\'").replace("%", "%%")
            key = row[2]
            if key == "SoundAuthor":
                key = "sa"
            elif key == "SoundLocation":
                key = "sl"
            elif key == "SoundMonth":
                key = "sm"
            elif key == "SoundTitle":
                key = "st"
            elif key == "BackgroundSpeciesAudio":
                key = "bsa"
            f1.write("<string name=\"%s%s\"><![CDATA[%s]]></string>" % (key, row[0], value))
    f1.write("</resources>")
    con.close()
    return

def songStrings():
    for l in LANGUAGES:
        generateStringForSongs(l[0], l[1])
    return

def songsFile():
    if not(os.path.exists(SONG_FOLDER)):
        sys.exit()
    clean()
    songs()
    return

#######################
## Execution
#######################
songsFile()
#songStrings()
#songsModel()