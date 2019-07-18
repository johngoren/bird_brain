# Data Sync

There are a few scripts that we use to maintain the data of the app.
1. ```database.py```.
2. ```annotations.py``` and ```annotations_fixes.py```.
3. ```filters.py```.
4. ```images.py```.
5. ```songs.py```.

## 1. Main database generation logic:

Script ```database.py```. 

Ids used are from ```select entity_id from strix_entities;```

Script takes data from filter db ('bird_guide_filter.db'), entity db ('Strix_BIRDGUIDE.db'), collins db ('distribution-WP.sqlite'), bto db ('BTOSearch.db') and Similar_species.csv to generate the following schema for the main database of the app.

```
CREATE TABLE Bto (
    id     INT,
    region TEXT,
    season INT
);

CREATE TABLE Collins (
    id     INT,
    region INT,
    season INT
);

CREATE TABLE Morphs (
    id    INT,
    morph TEXT
);

CREATE TABLE Scores (
    id      INT,
    score   INT,
    code    TEXT,
    morph   TEXT,
    taxcode TEXT
);

CREATE TABLE Similarities (
    id           INT,
    morph        TEXT,
    similarId    INT,
    similarMorph TEXT,
    priority     INT
);
```

## 2. Annotations 

Annotations are stored into the asset folder of the app in a json format. The name of the file match the id from the generated database (form script 1).

Sources used to run the script are:  annotations files, frame info file and the generated database.

NOTE: annotations_fixes script is used to automatically convert some of the notations used by ios that are not supported in android.

## 3. Filters

Filters are stored as generated classes containing ids references for translation and android strings files containing translations.

Script runs in two steps: 
1. First creates the strings files (data/filters/*txt) from extracted txt files from ios source. The scripts works on them to translate them into and understandable xml.
2. Genarate classes that contains objects easily used by the app in various scenario.

NOTE: Script uses: Filter db, collings db, bto db and entity db.

## 4. Images

Images script is used to collect and organize images from various sources into assets of the app:

- families
- mapThumbnails
- filterMapCollins
- filter_bto_map

Images script is used to collect and organize images from various sources into apklib (This was done once and not updated yet):

- species
- morphs
- mapImages
- mapCollins

NOTE: reduceImages was added for development before we used the apklib.

## 5. Songs

Songs Script is used to create a java model of the songs and prepare songs for the apklib.
Data is collected from '../data/songs/' and entity database.


## Scale images

For development it is raccomended to remove songs from asset folder and reduce the images size. To reduce image size you need to run:

```
python images.py --scale 300
```

With this images will be scaled down to a width of 300.


For this though you will need pip and python. If you want to resize image you also need [python-resize-image](https://pypi.python.org/pypi/python-resize-image) library : 
```
pip install python-resize-image
```

## Using databases

Some of the databases as file of the data are sqlite you can check them out with: [sqlitebrowser](https://github.com/sqlitebrowser/sqlitebrowser)