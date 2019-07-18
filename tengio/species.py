import sqlite3
import os.path
import sys

DATA_FOLDER = '../data'
APP_FOLDER = '../app'
ENTITIES_DB = '%s/Strix_BIRDGUIDE.db' % DATA_FOLDER
VALUES_FOLDER = '%s/src/main/res/values' % APP_FOLDER
LANGUAGES = [
    ['en', '%s/' % VALUES_FOLDER],
    ['de', '%s-de/' % VALUES_FOLDER],
    ['fr', '%s-fr/' % VALUES_FOLDER],
    ['nb', '%s-no/' % VALUES_FOLDER],
    ['sv', '%s-sv/' % VALUES_FOLDER]
]
SECONDARY_LANGUAGES = [
    ['da', '%s-da/' % VALUES_FOLDER],
    ['en-GB', '%s-en-rGB/' % VALUES_FOLDER],
    ['es', '%s-es/' % VALUES_FOLDER],
    ['et', '%s-et/' % VALUES_FOLDER],
    ['fi', '%s-fi/' % VALUES_FOLDER],
    ['hu', '%s-hu/' % VALUES_FOLDER],
    ['in', '%s-ia/' % VALUES_FOLDER],
    ['it', '%s-it/' % VALUES_FOLDER],
    ['nl', '%s-nl/' % VALUES_FOLDER],
    ['pl', '%s-pl/' % VALUES_FOLDER],
    ['pt-PT', '%s-pt-rPT/' % VALUES_FOLDER],
    ['ru', '%s-ru/' % VALUES_FOLDER],
    ['sk', '%s-sk/' % VALUES_FOLDER],
    ['cs', '%s-cs/' % VALUES_FOLDER],
    ['is', '%s-is/' % VALUES_FOLDER],
    ['lt', '%s-lt/' % VALUES_FOLDER],
    ['hu', '%s-hu/' % VALUES_FOLDER],
    ['bg', '%s-bg/' % VALUES_FOLDER]
]
NEW_SPECIES = "ns(%s,%s,%s,%s,%s,%s,%s,%s,%s),"

def generateStringsForEntities( language, directoryName ):
    if not os.path.exists(directoryName):
        os.makedirs(directoryName)

    f1 = open("%sentities.xml" % directoryName, 'wb')
    f1.write("<resources xmlns:tools=\"http://schemas.android.com/tools\" tools:ignore=\"all\">\n")
    if os.path.exists(DATA_FOLDER):
        con = sqlite3.connect(ENTITIES_DB)
        c = con.cursor()
        c.execute("SELECT attribute_key, attribute_value, strix_entities.entity_id FROM strix_entity_attributes left join strix_entities on strix_entities.entity_id = strix_entity_attributes.entity_id where attribute_language_code = '%s' and attribute_key in ('Name', 'NameSc', 'Identification', 'Summary', 'Voice', 'Size', 'StatusCode')" % language)
        for row in c:
            t = row[0].encode('utf-8').lower().replace("summary", "su").replace("identification", "i").replace("voice", "v").replace("statuscode", "sc").replace("size", "s").replace("name", "n").replace("namesc", "sn")
            u = row[1].encode('utf-8').replace("&", "&amp;").replace("&amp;lt;", "&lt;").replace("\'", "\\'").replace("%", "%%")
            n = "s%s" % row[2]

            if t == "su" or t == "i" or t == "v" or t == "sc" or t == "s":
                f1.write("<string name=\"%s%s\"><![CDATA[%s]]></string>" % (n, t, u))
            else:
                f1.write("<string name=\"%s%s\">%s</string>" % (n, t, u))
        con.close()
    f1.write("</resources>")
    return

def generateStringForScientificNameOfSpecies(directoryName):
    print directoryName
    if not os.path.exists(directoryName):
        print "do not exists"
        os.makedirs(directoryName)

    print "exists"
    f1 = open("%sspecies_sc.xml" % directoryName, 'wb')
    print "opening file"
    f1.write("<resources xmlns:tools=\"http://schemas.android.com/tools\" tools:ignore=\"all\">\n")
    if os.path.exists(DATA_FOLDER):
        print "getting database connection"
        con = sqlite3.connect(ENTITIES_DB)
        c = con.cursor()
        c.execute("SELECT 'sn', attribute_value, strix_entities.entity_id FROM strix_entity_attributes left join strix_entities on strix_entities.entity_id = strix_entity_attributes.entity_id where attribute_language_code = 'sc' and attribute_key = 'Name'");
        print "connection running cycle"
        for row in c:
            print row
            t = row[0].encode('utf-8').lower()
            u = row[1].encode('utf-8').replace("&", "&amp;").replace("\'", "\\'").replace("%", "%%")
            n = "s%s" % row[2]

            f1.write("<string name=\"%s%s\">%s</string>" % (n, t, u))
        con.close()

    f1.write("</resources>")
    return

def entitiesStrings():
    for l in LANGUAGES:
        generateStringsForEntities(l[0], l[1])
    for l in SECONDARY_LANGUAGES:
        generateStringsForEntities(l[0], l[1])
    return

def write(content):
    #print content
    fn.write(content)
    return

def header():
    write("package com.natureguides.birdguide.model.data;\n")
    write("\n")
    return

def secondaryHeader():
    write("// CHECKSTYLE SUPPRESS 100 LINES\n")
    write("import static com.natureguides.birdguide.R.string.*;\n\n")
    write("import static java.util.Arrays.asList;\n")
    write("import java.util.List;\n\n")
    write("import static com.natureguides.birdguide.model.Species.ns;\n")
    write("import com.natureguides.birdguide.model.TaxonomyGroup;\n\n")
    write("public final class EntitiesDataModel {\n")
    return

def footer():
    write("}")
    return

def isInStringsFile(value, file_path):
    """Controls if value is in strings file"""
    strings_file = file(file_path)
    for line in strings_file:
        if value in line:
            return True
    print "String value for %s is missing" % (value)
    return False

def wrapString(r, suffix, filePath):
    r = r.replace("species", "s").replace("family", "f")
    check = "\"%s%s\"" % (r, suffix)
    if isInStringsFile(check, filePath):
        return "%s%s" % (r, suffix)
    return "nf"

def speciesnamesc(ref):
    return wrapString(ref, "sn", '%s/species_sc.xml' % VALUES_FOLDER)

def namesc(r):
    return wrapString(r, "sn", '%s/entities.xml' % VALUES_FOLDER)

def voice(r):
    return wrapString(r, "v", '%s/entities.xml' % VALUES_FOLDER)

def identification(r):
    return wrapString(r, "i", '%s/entities.xml' % VALUES_FOLDER)

def summary(r):
    return wrapString(r, "su", '%s/entities.xml' % VALUES_FOLDER)

def name(r):
    return wrapString(r, "n", '%s/entities.xml' % VALUES_FOLDER)

def size(r):
    return wrapString(r, "s", '%s/entities.xml' % VALUES_FOLDER)

def statuscode(r):
    return wrapString(r, "sc", '%s/entities.xml' % VALUES_FOLDER)

def imageName(r):
    return r.replace("species_", "s_")

def getIllustrator(con, id):
    sc = con.cursor()
    sc.execute('select attribute_value FROM strix_entity_attributes where attribute_key = \'Illustrator\' and entity_id = %s;' % id)
    for row in sc:
        if row[0] == 'KM':
            return 1
        elif row[0] == 'DZ':
            return 2
    return 0

def species(con, id, r):
    r = "s%s" %id
    return NEW_SPECIES % (id, name(r), speciesnamesc(r), identification(r), summary(r), voice(r), size(r), statuscode(r), getIllustrator(con, id))

def taxonomyWithChildren(id, r):
    r = "s%s" %id
    return "new TaxonomyGroup(%s,%s,%s,%s," % (id, name(r), namesc(r), summary(r))

def taxonomyWithNoChildren(id, r):
    r = "s%s" %id
    return "new TaxonomyGroup(%s,%s,%s,%s,new ArrayList<>())," % (id, name(r), namesc(r), summary(r))

def reducedTaxonomy(id, r, children):
    r = "s%s" %id
    return "new TaxonomyGroup(%s,%s,nf,%s,%s)," % (id, name(r), summary(r), children)

def lastLevelChildren(con, id, reference, groupReference):
    sc = con.cursor()
    sc.execute('select entity_reference, entity_type, entity_id from strix_entities where parent_entity_id = %s order by entity_order;' % id)
    content="asList("
    for row in sc:
        sn = row[0].encode('utf-8').replace(".", "_").lower()
        sid = row[2]
        if groupReference == "order_accidentals":
            content += species(con, sid, sn)
        else:
            content += species(con, sid, sn)
    content = content[:-1]
    content+=")"
    return content

def taxonomyGroupWithChildren(con, id, reference):
    content = taxonomyWithChildren(id, reference)
    sc = con.cursor()
    sc.execute('select entity_reference, entity_type, entity_id from strix_entities where parent_entity_id = %s order by entity_order;' % id)
    content += "asList("
    for row in sc:
        sn = row[0].encode('utf-8').replace(".", "_")
        sid = row[2]
        if row[1] == "taxon.species":
            content += species(con, sid, sn)
        else:
            children = lastLevelChildren(con, sid, sn, reference)
            content+= reducedTaxonomy(sid, sn, children)

    content = content[:-1]
    content += ")),"
    return content

def taxonomy():
    con = sqlite3.connect(ENTITIES_DB)
    c = con.cursor()
    c.execute('select entity_reference, entity_id from strix_entities where parent_entity_id = 517012 order by entity_order;')
    content = "\n"
    content += "  public static final List<TaxonomyGroup> TAXONOMY_GROUPS = asList("
    for row in c:
        n = row[0].encode('utf-8').replace(".", "_")
        id = row[1]
        content += taxonomyGroupWithChildren(con, id, n)
    content = content[:-1]
    if content.endswith(","):
        content = content[:-1]
    content += ");"
    write(content)
    return

def taxonomiesAndSpecies():
    header()
    if not os.path.exists(DATA_FOLDER):
        sys.exit()
    secondaryHeader()
    taxonomy()
    footer()
    return


#######################
## Execution
#######################

entitiesStrings()
# fn = open('%s/src/main/java/com/natureguides/birdguide/model/data/EntitiesDataModel.java' % APP_FOLDER, 'wb')
# generateStringForScientificNameOfSpecies('%s/' % VALUES_FOLDER)
# taxonomiesAndSpecies()
