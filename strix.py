import sqlite3
import sys

class StrixDatabase:
    def __init__(self, path):
        if path is None:
            sys.exit("Missing database path.")
        self.db_path = path

    def lookup_ref(self, id):
        query = f'SELECT entity_reference FROM strix_entities where entity_id={id}'
        c = self.get_cursor()

        ref = None
        
        for row in c.execute(query):
            ref = row[0]

        return ref

    def get_species_id_list(self):
        query = 'SELECT entity_id FROM strix_entities WHERE entity_type="taxon.species"'
        c = self.get_cursor()

        rows = c.execute(query)
        return [i[0] for i in rows]

    def get_all_song_refs(self):
        query = f'SELECT entity_reference FROM strix_entities WHERE entity_type="species.song"'
        c = self.get_cursor()

        rows = c.execute(query)
        return [i[0] for i in rows]

    def get_song_refs_for_species(self, id):
        query = f'SELECT entity_reference FROM strix_entities WHERE entity_type="species.song" AND parent_entity_id={id}'
        c = self.get_cursor()

        rows = c.execute(query)
        return [i[0] for i in rows]

    def get_cursor(self):
        conn = sqlite3.connect(self.db_path)
        return conn.cursor()

