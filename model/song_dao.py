from sqlalchemy import text

class SongDao:
    def __init__(self,database):
        self.db = database

    def insert_song(self,req):
        return self.db.execute(text("""
        INSERT INTO songs (title,artist,e_label,v_label,mood_tag)
        VALUES (:title,:artist,:e_label,:v_label,:mood_tag)
        """),req).lastrowid

    def get_song_list(self,query):
        query = f'%{str(query).lower()}%'
        song_list = self.db.execute(text("""
        SELECT * FROM songs
        WHERE artist LIKE :query OR title LIKE :query
        ORDER BY id
        """),{"query": query}).fetchall()

        return [{
            "title":song["title"],
            "artist":song["artist"],
            "mood_tag": song["mood_tag"],
            "e_label":song["e_label"],
            "v_label":song["v_label"],
            "mood_tag":song["mood_tag"],
            "id": song["id"]
        } for song in song_list]

    def get_song_list_with_mood_tag(self,query):
        target_songs = self.db.execute(text("""
        SELECT id,title, artist, mood_tag FROM songs
        WHERE mood_tag = :mood_tag
        ORDER BY id
        LIMIT 30
        """),{"mood_tag":query}).fetchall()

        return [{
            "title":song["title"],
            "artist":song["artist"],
            "mood_tag": song["mood_tag"],
            "id": song["id"]
        } for song in target_songs]

    def get_mood_tags(self):
        mood_tags = self.db.execute(text("""
        SELECT DISTINCT mood_tag FROM songs
        """)).fetchall()

        return [{
            "tag":tag["mood_tag"] 
        }for tag in mood_tags]