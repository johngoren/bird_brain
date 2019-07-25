import os
import config
import pdb

# Returns list of all song files in the expansion pack dir.

def get_song_files_from_disk():
    songs_path = config.PATH_SONGS
    filenames = os.listdir(songs_path)
    return list(filter(lambda x: x[0] is not ".", filenames))
