import os

PACKAGE = "com.natureguides.birdguide"
ANDROID_STUDIO_PROJECTS_PATH = os.environ['STUDIO_PROJECT_PATH']
PLATFORM_TOOLS_PATH = os.environ['PLATFORM_TOOLS_PATH']
PROJECT_DIR = "/home/john/Dropbox/natureguides"

PATH_APP = f'{ANDROID_STUDIO_PROJECTS_PATH}/collins'
PATH_APP_ASSETS = f'{PATH_APP}/app/src/main/assets'

ADB = f'{PLATFORM_TOOLS_PATH}/adb.exe'

# TODO: Update
NUM_SPECIES_IMAGES = 792

OBB_VERSION = 119
OBB_FILENAME = f'main.{OBB_VERSION}.{PACKAGE}.obb'

PATH_OBB_SOURCE = f'{PROJECT_DIR}/assets/expansion'
PATH_OBB_CREATION = f'{PATH_OBB_SOURCE}/{OBB_FILENAME}'
PATH_OBB_DESTINATION_DIR = f'/storage/emulated/0/Android/obb/{PACKAGE}'
PATH_OBB_DESTINATION = f'{PATH_OBB_DESTINATION_DIR}/{OBB_FILENAME}'

PATH_SONGS = f'{PATH_OBB_SOURCE}/songs'
PATH_FAMILY = f'{PATH_OBB_SOURCE}/images/family'
PATH_SPECIES_IMAGES_DIR = f'{PATH_OBB_SOURCE}/images/species'
PATH_SPECIES_IMAGES_FULL = f'{PATH_SPECIES_IMAGES_DIR}/full'
PATH_SPECIES_IMAGES_THUMBNAIL = f'{PATH_SPECIES_IMAGES_DIR}/thumbs'
PATH_PLUMAGES_IMAGES = f'{PATH_OBB_SOURCE}/images/plumages'
PATH_MAPS_BRITAIN = f'{PATH_OBB_SOURCE}/images/maps/bto'
PATH_MAPS_COLLINS = f'{PATH_OBB_SOURCE}/images/maps/collins'

HD_ORIGINALS_PATH = f'/Users/johngorenfeld/Dropbox/natureguides/assets/HD/Europe'

DB_VERSION = 506
DB_FILENAME = f'Strix_BIRDGUIDE_v{DB_VERSION}.db'
STRIX_DB_PATH = f'{PATH_APP_ASSETS}/databases/{DB_FILENAME}'
