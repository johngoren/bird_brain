import os
import config

# Returns list of all song files in the expansion pack dir.

def get_songs():
    songs_path = config.PATH_SONGS
    return os.listdir(songs_path)    