import shutil
import os
import sys
import os.path
import sqlite3
import xml.etree.ElementTree
import nameutils
import json
import config

base_root = config.base_root
dataFolder = config.data_folder
frameFile = config.frame_file
database = config.database_tengio_path
assetFolder = config.asset_folder

def clean(locale):
    if os.path.exists('%s%s' % (assetFolder, locale)):
        shutil.rmtree('%s%s' % (assetFolder, locale))
    return

def parseText(c):
    frame = c.getchildren()[3].text.replace("{", "").replace("}", "")
    alignment = 0
    text = c.getchildren()[5].text
    if text == None:
        text = ""
    else:
        if "class=\"center" in text or "class=\"centre" in text:
            alignment = 1
        elif "class=\"right" in text:
            alignment = 2
        print text
        text = text.replace("</p><p>", "<br>")
        text = text.replace("</p><p class=\"right\">", "<br>")
        text = text.replace("</p><p class=\"center\">", "<br>")
        print text
        text = text.replace("<p class=\"left\">", "").replace("<p class=\"centre\">", "").replace("<p class=\"center\">", "").replace("</p>", "").replace("<p class=\"right\">", "").replace("<p>", "").replace("\n", "<br>")

    parts = frame.split(", ")
    x1 = round(float(parts[0][:6]), 4)
    y1 = round(float(parts[1][:6]), 4)
    x2 = round(float(parts[2][:6]), 4)
    y2 = round(float(parts[3][:6]), 4)
    text = text.replace("</b>(", "</b><br>(")
    text = text.replace("\u00ad-", "-<br>")
    text = text.replace("-\u00ad", "-<br>")
    fontscale = float(c.getchildren()[1].text[:6])
    return {'content':text,'fontscale':fontscale,'x1':x1,'y1':y1,'x2':x2,'y2':y2,'alignment':alignment} 

def parseLine(c):
    endPoint = c.getchildren()[1].text.replace("{", "").replace("}", "")
    startPoint = c.getchildren()[3].text.replace("{", "").replace("}", "")
    ends = endPoint.split(", ")
    stars = startPoint.split(", ")
    x1 = round(float(ends[0][:8]), 4)
    y1 = round(float(ends[1][:6]), 4)
    x2 = round(float(stars[0][:6]), 4)
    y2 = round(float(stars[1][:6]), 4)
    return {'x1':x1,'y1':y1,'x2':x2,'y2':y2}

def getFrame(file):
    # species.upupa_epops.plist
    print file
    e = xml.etree.ElementTree.parse(frameFile).getroot()
    nodes = e.findall('./dict/')
    for i in range(0,len(nodes),2):
        first = nodes[i]
        second = nodes[i+1]
        if file.replace('.plist', '') == first.text:
            frameString = second.findall('string')[-1].text
            parts = frameString.replace("{", "").replace("}", "").split(", ")
            return parts
    return

def annotations(locale):
    files = os.listdir("%s%s" % (dataFolder, locale))
    for f in files:
        if f != ".DS_Store":
            print "Parsing : %s" % f
            e = xml.etree.ElementTree.parse("%s%s/%s" % (dataFolder, locale, f)).getroot()
            annotations = []
            frame = getFrame(f)
            for child in e.findall('array'):
                for c in child.getchildren():
                    for i in range(0,len(c.getchildren()),2):
                        first = c.getchildren()[i]
                        second = c.getchildren()[i+1]
                        if first.text == "Type" and second.text == "text":
                            obj = parseText(c)
                            annotations.append({'c': obj['content'], 'f': obj['fontscale'], 'x1': obj['x1'], 'y1': obj['y1'], 'x2': obj['x2'], 'y2': obj['y2'], 'a': obj['alignment'] })
                        elif first.text == "Type" and second.text == "line":
                            obj = parseLine(c)
                            annotations.append({'x1': obj['x1'], 'y1': obj['y1'], 'x2': obj['x2'], 'y2': obj['y2']})

            if not os.path.exists('%s%s' % (assetFolder, locale)):
                os.makedirs('%s%s' % (assetFolder, locale))
            print '%s%s/%s.json' % (assetFolder, locale, nameutils.getImageFileNameFromPlistFile(f))
            with open('%s%s/%s.json' % (assetFolder, locale, nameutils.getImageFileNameFromPlistFile(f)) , 'w') as outfile:
                print frame
                json_string = json.dumps({
                    'x1': round(float(frame[0][:6]), 4), 
                    'y1': round(float(frame[1][:6]), 4), 
                    'x2': round(float(frame[2][:6]), 4), 
                    'y2': round(float(frame[3][:6]), 4), 
                    'annotations': annotations
                    }, separators=(',',':'))
                outfile.write(json_string)

    return annotations

def insertAllAnnotationsForLocale(c, locale):
    c.execute("DROP TABLE IF EXISTS annotations_%s" % locale)
    columnsDesc = "_id INTEGER PRIMARY KEY AUTOINCREMENT, reference TEXT, content TEXT, fontscale TEXT, x1 TEXT, y1 TEXT, x2 TEXT, y2 TEXT, alignment INTEGER"
    c.execute("CREATE TABLE annotations_%s(%s)" % (locale, columnsDesc))
    for a in annotations(locale):
        columns = "reference, content, fontscale, x1, y1, x2, y2, alignment"
        values = "\"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\"" % (a['ref'], a['content'], a['fontscale'], a['x1'], a['y1'], a['x2'], a['y2'], a['alignment']) 
        c.execute("INSERT INTO annotations_%s (%s) VALUES(%s)" % (locale, columns, values))


#######################
## Execution
#######################

locales = ['en','de','fr','nb','sv']

if not(os.path.exists(dataFolder)): 
    print "Could not find data folder at %s" % dataFolder
    sys.exit()
for l in locales:
    print "Processing annotations for locale %s" % locals
    clean(l)
    annotations(l)

# getFrame('species.upupa_epops.plist') 
