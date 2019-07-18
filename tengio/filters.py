import sqlite3
import os
import os.path
import hashlib

DATA_FOLDER = "../data/"
APP_FOLDER = "../app"
ASSET_FOLDER = '../app/src/main/assets/databases/'
APP_DB = sqlite3.connect('%sbird-guide.db' % ASSET_FOLDER)
VALUES_FOLDER = '%s/src/main/res/values' % APP_FOLDER
LANGUAGES = [
    ['en', '%s/' % VALUES_FOLDER],
    ['de', '%s-de/' % VALUES_FOLDER],
    ['fr', '%s-fr/' % VALUES_FOLDER],
    ['no', '%s-no/' % VALUES_FOLDER],
    ['sv', '%s-sv/' % VALUES_FOLDER]
]
FILTER_DB = '%sbird_guide_filter.db' % DATA_FOLDER
COLLINS_DB = sqlite3.connect('%smaps-collins/Filter/distribution-WP.sqlite' % DATA_FOLDER)
ENTITY_DB = sqlite3.connect('%sStrix_BIRDGUIDE.db' % DATA_FOLDER)
ENTITY_CURSOR = ENTITY_DB.cursor()

def get_id(reference):
    """Get id from entity table given a reference"""
    statement = 'select ENTITY__id from strix_entities where ENTITY__reference = \'%s\' limit 1'
    ENTITY_CURSOR.execute(statement % reference)
    return ENTITY_CURSOR.fetchone()[0]

def filters_strings(language):
    """Create string for filters and a specific language"""
    if not os.path.exists(language[1]):
        os.makedirs(language[1])
    with open("%sfilters/filters_%s.txt" % (DATA_FOLDER, language[0])) as filter_source:
        content = filter_source.readlines()
    filters_file = open("%sfilters.xml" % language[1], 'wb')
    header = "<resources xmlns:tools=\"http://schemas.android.com/tools\" tools:ignore=\"all\">\n"
    filters_file.write(header)
    for line in content:
        line = line.replace("&", "&amp;")
        line = line.replace("\"FILTER_CRITERION_TITLE_", "<string name=\"ft")
        line = line.replace("\"FILTER_CRITERION_OPTION_TITLE_", "<string name=\"fot")
        line = line.replace("= \"", ">")
        line = line.replace("\";", "</string>")
        filters_file.write(line)
    filters_file.write("</resources>")
    return

def collins_map_strings(language):
    """Create string for filters for collins map and a specific language"""
    if not os.path.exists(language[1]):
        os.makedirs(language[1])
    filters_file = open("%sfilters_collings.xml" % language[1], 'wb')
    header = "<resources xmlns:tools=\"http://schemas.android.com/tools\" tools:ignore=\"all\">\n"
    filters_file.write(header)
    ENTITY_CURSOR.execute("""
    select strix_entities.entity_id, attribute_value
    from strix_entities
    left join strix_entity_attributes on strix_entity_attributes.entity_id = strix_entities.entity_id
    where attribute_key = 'CollinsMapRegion' and attribute_language_code = '%s';
    """ % language[0])
    # insert_statement = "INSERT INTO Collins VALUES(%s, %s, %s)"
    for row in ENTITY_CURSOR:
        cleaned = row[1].encode('utf-8').replace("'", "\\'").strip()
        value = "<string name=\"fcm%s\"><![CDATA[%s]]></string>" % (row[0], cleaned)
        filters_file.write(value)
    filters_file.write("</resources>")
    return

def prepare_filter_strings():
    """Prepare filter string for all languages"""
    for language in LANGUAGES:
        filters_strings(language)
        collins_map_strings(language)
    return

def add_filter_option(con, option_id):
    """Prepare filter option string"""
    cursor = con.cursor()
    cursor.execute('select * from options where criteriaId = %s;' % option_id)
    content = "asList("
    for row in cursor:
        content += "fo(%s,fot%s)," % (row[0], row[2])
    content = content[:-1]
    content += ")"
    return content

def collins_regions():
    """Prepare filters string for collings regions"""
    cursor = APP_DB.cursor()
    cursor.execute("select region from Collins group by region")
    content = "asList("
    for row in cursor:
        content += "fo(%s,fcm%s)," % (row[0],row[0])
    content = content[:-1]
    content += ")"
    return content

def bto_regions():
    """Prepare filters string for bto regions"""
    cursor = APP_DB.cursor()
    cursor.execute("select region from Bto group by region")
    content = "asList("
    for row in cursor:
        if row[0] != "NW":
            md5 = hashlib.md5()
            md5.update(row[0].replace("/", "_"))
            content += "fo(%s, \"%s\")," % (abs(int(md5.hexdigest(), 16)) % (10 ** 5), row[0])
    content = content[:-1]
    content += ")"
    return content

def prepare_filters_model():
    """Prepare filters model"""
    content = "package com.natureguides.birdguide.model.data;\n\n"
    content += "// CHECKSTYLE SUPPRESS 20 LINES\n"
    content += "import static com.natureguides.birdguide.R.string.*;\n\n"
    content += "import static java.util.Arrays.asList;\n"
    content += "import java.util.ArrayList;\n"
    content += "import java.util.List;\n\n"
    content += "import com.natureguides.birdguide.model.Filter;\n"
    content += "import static com.natureguides.birdguide.model.FilterOption.*;\n"
    content += "import static com.natureguides.birdguide.model.Filter.FilterType.*;\n\n"
    content += "public final class FiltersDataModel {\n"
    content += "public static final List<Filter> FILTERS = asList("
    print FILTER_DB
    con = sqlite3.connect(FILTER_DB)
    cursor = con.cursor()
    cursor.execute('select * from Criteria order by Criteria."Order";')
    content += "new Filter(filter_region_and_season, asList("
    content += "new Filter(filter_collins, asList("
    content += "new Filter(\"collins_region\",filter_region,MULTIPLE_CHOICE,.0, "
    content += collins_regions()
    content += "),"
    content += "new Filter(\"collins_season\",filter_season,CHOICE,.0,asList("
    content += "fo(SEASON_ALL,filter_option_any)"
    content += ",fo(SEASON_BREEDING,filter_option_breeding)"
    content += ",fo(SEASON_WINTERING,filter_option_wintering))))),"
    content += "new Filter(filter_bto, asList("
    content += "new Filter(\"bto_region\",filter_region,MULTIPLE_CHOICE,.0, "
    content += bto_regions()
    content += "),"
    content += "new Filter(\"bto_season\",filter_season,CHOICE,.0,asList("
    content += "fo(SEASON_ALL,filter_option_any)"
    content += ",fo(SEASON_BREEDING,filter_option_breeding)"
    content += ",fo(SEASON_WINTERING,filter_option_wintering)))))"
    content += ")),"
    filter_string = "new Filter(\"%s\",ft%s,%sCHOICE,%s,%s),"
    for row in cursor:
        ref = row[5]
        options = add_filter_option(con, row[0])
        filter_type = ""
        if row[3] != "Choice":
            filter_type = "MULTIPLE_"
        content += filter_string % (ref, ref, filter_type, row[6], options)
    content = content[:-1]
    content += ");\n}"  
    model_class = '%s/src/main/java/com/natureguides/birdguide/model/data/FiltersDataModel.java'
    filters_file = open(model_class % APP_FOLDER, 'wb')
    filters_file.write(content)
    return

#######################
## Execution
#######################

prepare_filter_strings()
prepare_filters_model()
