import os
import sys
import os.path
import zipfile

currentRoot = os.getcwd()
baseRoot = "./"
if(currentRoot.endswith("scripts")):
    baseRoot = "../"

assetFolder = '%sapp/src/main/assets/annotations/' % baseRoot

def replaceInAnnotation(annotation, source, destination):
    annotation_file = '%s%s.json' % (assetFolder, annotation)
    with open(annotation_file, 'r') as file :
        filedata = file.read()

    filedata = filedata.replace(source, destination)
    with open(annotation_file, 'w') as file:
        file.write(filedata)
    return

# def zipdir(path, destination):
#     zf = zipfile.ZipFile(destination, mode='w')
#     for files in os.walk(path):
#         for file in files:
#             zf.write(file)
# zipdir("%sapp/src/main/assets/annotations/en" % baseRoot, "%sapp/src/main/assets/annotations/en.zip" % baseRoot)
# zip everything up???

#######################
## Execution
#######################
replaceInAnnotation("en/s_517208", "predomi\u00ad-nant\u00adly dark but can appear light against the sky", "predomi\u00ad-<br> nant\u00adly dark but can appear light against the sky" )
#mute swan
replaceInAnnotation("en/s_517020", "WHITE-FRONTED<b><i></i></b><b><i>albifrons</i></b>", "WHITE-FRONTED<b><i></i></b><br><b><i>albifrons</i></b>")
replaceInAnnotation("en/s_517071", "all young scoters have a pale belly", "all young <br>scoters have a pale belly")
replaceInAnnotation("en/s_517075", "head held high,rather small wingsbeating vigorously", "head held high, <br>rather small wings<br>beating vigorously")
replaceInAnnotation("en/s_517144", "Zino\u2019s is close to Manx Shear-water in size; Fea\u2019s is a little bigger", "Zino\u2019s is<br>close to<br>Manx Shear-<br>water in size;<br>Fea\u2019s is a little bigger")
#Flamingo
replaceInAnnotation("en/s_517193", "bright crimson-red", "bright<br>crimson-red") 
#Rupplells Vulture
replaceInAnnotation("en/s_517201", "coverts dark with distinct pale bar in juv. (older birds attain several distinct bars)", "coverts dark with distinct<br>pale bar in juv. (older<br> birds attain several<br> distinct bars)")
replaceInAnnotation("en/s_517201", "lacks Griffon\u2019s typical rusty underside", "lacks<br> Griffon\u2019s<br> typical rusty underside")
#Imperial eagle
replaceInAnnotation("en/s_517212", "dark throat", "dark<br>throat")
replaceInAnnotation("en/s_517212", "resem-bles ad. Golden!", "resem-<br>bles ad.<br> Golden!")
#Spanish Imperial Eagle
replaceInAnnotation("en/s_517213", "body and coverts soon bleach to pale tawny\u2014very similar to juv. Tawny Eagle!", 
    "body and<br>coverts soon bleach<br>to pale tawny\u2014very<br>similar to juv. Tawny Eagle!")
#Lesser Spotted eagle
replaceInAnnotation("en/s_517214", "STEPPE, subad.", "STEPPE,<br> subad.")
replaceInAnnotation("en/s_517214", "LESSER SPOTTED", "LESSER<br>SPOTTED")
#Moustached wabler
replaceInAnnotation("en/s_517678", "              narrow black mous\u00adtachial             stripe and grey        ear-coverts", "narrow black<br>mous\u00adtachial<br>stripe and grey<br>ear-coverts")
#Syrian woodpecker
replaceInAnnotation("en/s_517522", "breeds in mature deciduous woods in cul-tivated open country; also in villages and towns", "breeds<br>in mature<br>deciduous<br>woods in cul-<br>tivated open country; also in villages<br> and towns")

######################################
# Alignment manual fixes
######################################
replaceInAnnotation("en/s_517049", "\"y1\":0.0006", "\"y1\":0.01")
replaceInAnnotation("en/s_517136", "\"y1\":0.0,", "\"y1\":0.01,")
replaceInAnnotation("en/s_517141", "\"y1\":0.0,", "\"y1\":0.01,")
replaceInAnnotation("en/s_517129", "\"y1\":0.0,", "\"y1\":0.01,")
replaceInAnnotation("en/s_517341", "\"y2\":0.7949", "\"y2\":0.7351")
replaceInAnnotation("en/s_517599", "\"y1\":0.106", "\"y1\":0.06")
replaceInAnnotation("en/s_517891", "\"x2\":0.0908", "\"x2\":0.08")
replaceInAnnotation("en/s_517891", "\"x2\":0.8655,\"x1\":0.1181", "\"x2\":0.835,\"x1\":0.1225")