import os
import sys
import os.path
import zipfile
import shutil

imageFolder = '../app/src/main/assets/families/%s/images/'

def move_images(language):
    folder = imageFolder % language
    print folder
    images = os.listdir(folder)
    for f in images:
        if f != ".DS_Store" and f != ".gitignore" and "@2x" in f:
            final_name = f.replace("@2x.png", ".png")
            print "%s%s" % (folder, f), " ==> ", "%s%s" % (folder, final_name)
            shutil.move("%s/%s" % (folder, f), "%s/%s" % (folder, final_name))            
    return

# for l in ['en','de','fr','no','sv']:
#     move_images(l)