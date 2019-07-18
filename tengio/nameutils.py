import sqlite3

def getSpeciesId(ref):
    con = sqlite3.connect('../data/Strix_BIRDGUIDE.db')
    c = con.cursor()
    c.execute('select entity_id from strix_entities where entity_reference = \"%s\" order by entity_order;' % ref)
    for row in c:
        return row[0]
    print "%s not found in the database" % ref
    return "not_found"

def getImageFileNameFromPlistFile(fileName):
    sn = fileName.replace(".plist", "").replace(".", "_", 1).replace("species", "s").lower()
    parts = fileName.replace(".plist", "").split(' ', 2)
    id = getSpeciesId(parts[0])
    if id != "not_found":
        if len(parts) <= 2:
            return "s_%s" % id
        else:
            return "p_%s_%s" % (id, parts[2].replace("-", "_").replace(" ", "_"))
    return "not_found %s %s" % (id, fileName), parts

def getMorphNameFromFile(fileName):
    sn = fileName.replace(".", "_", 1).replace("species", "s").lower()
    parts = fileName.split(' ', 2)
    id = getSpeciesId(parts[0])
    if id != "not_found":
        return "p_%s_%s" % (id, parts[2].replace("-", "_").replace(" ", "_"))
    return "not_found"

def reduceSongFileName(fileName):
    f = fileName.replace(".wav.m4a", "")
    parts = f.split("_", 2)
    species = "species.%s" % parts[0].replace(".", "_").lower()
    if species == "species.aquila_nepalensis":
        species = "species.aquila_nipalensis"
    if species == "species.buteo_buteo_buteo":
        species = "species.buteo_buteo"
    if species == "species.charadrius_alexandrius":
        species = "species.charadrius_alexandrinus"
    if species == "species.charadrius_alexandrius":
        species = "species.charadrius_alexandrinus"
    if species == "species.gelochelidon_niltoica":
        species = "species.gelochelidon_nilotica"
    if species == "species.sylvia_ruppeli":
        species = "species.sylvia_rueppelli"
    if species == "species.larus_micahellis":
        species = "species.larus_michahellis"
    if species == "species.egretta_gullaris":
        species = "species.egretta_gularis"
    if species == "species.lagopus_lagopus_scotia":
        species = "species.lagopus_lagopus_scotica"
    if species == "species.scotocerca_inqieuta":
        species = "species.scotocerca_inquieta"
    if species == "species.sylvia_boring":
        species = "species.sylvia_borin"
    if species == "species.sylvia_curruca_halimodendri":
        species = "species.sylvia_curruca"
    id = getSpeciesId(species)
    if id != "not_found":
        return "%s_%s" % (id, parts[1])
    return f