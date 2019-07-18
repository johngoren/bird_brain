import shutil
import os
import sys
import os.path
import sqlite3
from PIL import Image
from resizeimage import resizeimage
import nameutils
import argparse
import hashlib

parser = argparse.ArgumentParser(prog='Data images import', description='Import images from data to asset folder.', epilog="Ok all done")
parser.add_argument('--scale', dest='scale', type=int, help='width to scale images with fix ratio')
parser.add_argument('--limit', dest='limit', type=int, help='width to scale images with fix ratio')
arguments = parser.parse_args()
assetFolder = '../app/src/main/assets/images/'
dataFolder = '../data'
entitiesDatabase = '%s/Strix_BIRDGUIDE.db' % dataFolder

def clean():
    for root, dirs, files in os.walk(assetFolder):
        for f in files:
            if f != ".gitignore" and f != "README":
                os.remove('%s/%s' % (assetFolder, f))
    return

def families():
    if arguments.limit != None:
        return
    familyFiles = os.listdir('%s/family-images/' % dataFolder)
    for f in familyFiles:
        if f != ".DS_Store":
            ref = f.replace("-192@3x", "").replace("jpg.jpg", "jpg").replace(".jpg", "").lower()
            id = nameutils.getSpeciesId(ref)
            if id != "not_found":
                shutil.copy("%s/family-images/%s" % (dataFolder, f), "%sf_%s.jpg" % (assetFolder, id))
                print "%s => %sf_%s.jpg" % (f, assetFolder, id)
    return

def species():
    speciesFiles = os.listdir('%s/illustrations/species/' % dataFolder)
    counter = 0
    for f in speciesFiles:
        if f != ".DS_Store":
            ref = f.replace(".jpg", "")
            id = nameutils.getSpeciesId(ref)
            if id != "not_found":
                if arguments.limit != None and arguments.limit < counter:
                    print "Imposed limit to %s" % arguments.limit
                    return
                counter = counter + 1
                shutil.copy("%s/illustrations/species/%s" % (dataFolder, f), "%ss_%s.jpg" % (assetFolder, id))
                print "%s => %ss_%s.jpg" % (f, assetFolder, id)
    return

def morphs():
    if arguments.limit != None:
        return
    speciesFiles = os.listdir('%s/illustrations/plumage/' % dataFolder)
    for f in speciesFiles:
        if f != ".DS_Store":
            name = nameutils.getMorphNameFromFile(f)
            if id != "not_found":
                shutil.copy("%s/illustrations/plumage/%s" % (dataFolder, f), "%s%s" % (assetFolder, name))
                print "%s => %s%s" % (f, assetFolder, name)
    return

def mapImages():
    speciesFiles = os.listdir('%s/maps-bto/Large/' % dataFolder)
    counter = 0
    for f in speciesFiles:
        if f != ".DS_Store" and "@2x" in f:
            parts = f.split('-', 1)
            id = nameutils.getSpeciesId(parts[0])
            if id != "not_found":
                if arguments.limit != None and arguments.limit < counter:
                    print "Imposed limit to %s" % arguments.limit
                    return
                counter = counter + 1
                t = parts[1].replace("@2x", "").replace("species.", "s_").replace("png.png", "png")
                shutil.copy("%s/maps-bto/Large/%s" % (dataFolder, f), "%sm_%s_%s" % (assetFolder, id, t))
                print "%s => %sm_%s_%s" % (f, assetFolder, id, t)

def mapThumbnails():
    speciesFiles = os.listdir('%s/maps-bto/Thumbs/' % dataFolder)
    counter = 0
    for f in speciesFiles:
        if f != ".DS_Store" and "@2x" in f:
            ref = f.replace("png.png", "png").replace("@2x.png", "")
            id = nameutils.getSpeciesId(ref)
            if id != "not_found":
                if arguments.limit != None and arguments.limit < counter:
                    print "Imposed limit to %s" % arguments.limit
                    return
                counter = counter + 1
                shutil.copy("%s/maps-bto/Thumbs/%s" % (dataFolder, f), "%smt_%s.png" % (assetFolder, id))
                print "%s => %smt_%s.png" % (f, assetFolder, id)

def mapCollins():
    if arguments.limit != None:
        return
    speciesFiles = os.listdir('%s/maps-collins/Images/' % dataFolder)
    for f in speciesFiles:
        if f != ".DS_Store":
            ref = f.replace(".jpg", "")
            id = nameutils.getSpeciesId(ref)
            if id != "not_found":
                shutil.copy("%s/maps-collins/Images/%s" % (dataFolder, f), "%scm_%s.jpg" % (assetFolder, id))
                print "%s => %scm_%s.jpg" % (f, assetFolder, id)

def filter_bto_map():
    if arguments.limit != None:
        return
    maps_files = os.listdir('%s/maps-bto/Squares/' % dataFolder)
    for f in maps_files:
        if f != ".DS_Store":
            ref = f.replace("png.png", "png").replace(".png", "")
            print ref
            md5 = hashlib.md5()
            md5.update(ref)
            id = str(abs(int(md5.hexdigest(), 16)) % (10 ** 5))
            shutil.copy("%s/maps-bto/Squares/%s" % (dataFolder, f), "%s%s.png" % (assetFolder, id))
            print "%s => %s%s.png" % (f, assetFolder, id)
    


def filterMapCollins():
    if arguments.limit != None:
        return
    regionsFiles = os.listdir('%s/maps-collins/Filter/Regions/' % dataFolder)
    for f in regionsFiles:
        if f != ".DS_Store" and "@2x" in f:
            ref = f.replace("png.png", "png").replace("@2x.png", "")
            id = nameutils.getSpeciesId(ref)
            if id != "not_found":
                shutil.copy("%s/maps-collins/Filter/Regions/%s" % (dataFolder, f), "%s%s.png" % (assetFolder, id))
                print "%s => %s%s.png" % (f, assetFolder, id)

def reduceImages():
    if arguments.scale == None:
        return
    images = os.listdir(assetFolder)
    for f in images:
        if f != ".DS_Store" and f != ".gitignore":
            imageFile = open('%s%s' % (assetFolder, f), 'r')
            img = Image.open(imageFile)
            img = resizeimage.resize_width(img, arguments.scale)
            img.save('%s%s' % (assetFolder, f), img.format)
            print '%s%s resized to %s' % (assetFolder, f, arguments.scale)
            imageFile.close()
    return

#######################
## Execution
#######################

if not(os.path.exists(dataFolder)):
    sys.exit()
clean()
families()
mapThumbnails()
filterMapCollins()
filter_bto_map()

# For outside apk
#species()
#morphs()
#mapImages()
#mapCollins()

reduceImages()
