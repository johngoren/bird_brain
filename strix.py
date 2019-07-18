import sqlite3


class StrixDatabase:
    def __init__(self, path):
        self.db_path = path

    def lookup_ref(self, id):
        query_key = f'SELECT entity_reference FROM strix_entities where entity_id={id}'
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()

        ref = None
        
        for row in c.execute(query_key):
            ref = row[0]

        return ref