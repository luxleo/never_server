from sqlalchemy import text

class LyricTagDao:
    def __init__(self,database):
        self.db = database

    def insert_lyric_tag(self,tag_name):
        return self.db.execute(text("""
        INSERT INTO lyric_tags (
            tag
        ) VALUES (:tag_name)
        """),{"tag_name":tag_name}).lastrowid
    
    def insert_map(self,tag_id,song_id):
        #추후에 tag_id,song_id db에 없으면 만들고 실행하게끔 하기
        check = self.db.execute(text("""
        INSERT INTO song_lyric_tag (song_id,tag_id)
        VALUES (:song_id,:tag_id)
        """),{
            "song_id":song_id,
            "tag_id":tag_id
        }).rowcount
        return check


    def get_song_list_of_lyric_tag(self,tag_id):
        target_songs = self.db.execute(text("""
        SELECT s.id, s.title,s.artist, lt.tag FROM((
            song_lyric_tag AS slt 
            INNER JOIN lyric_tags as lt ON slt.tag_id = lt.id
        )   INNER JOIN songs AS s ON slt.song_id = s.id
        ) WHERE lt.id = :tag_id
        ORDER BY s.id
        """),{"tag_id":tag_id}).fetchall()

        return [{
            "id":song["id"],
            "title":song['title'],
            "artist":song['artist'],
            "tag":song['tag']
        } for song in target_songs]

    def get_lyric_tags_of_song(self,song_id):
        tags = self.db.execute(text("""
        SELECT lt.id,lt.tag FROM((
            song_lyric_tag AS slt
            INNER JOIN songs AS s ON slt.song_id = s.id
        )   INNER JOIN lyric_tags as lt ON slt.tag_id = lt.id
        ) WHERE s.id = :song_id
        ORDER BY lt.id
        """),{"song_id": song_id}).fetchall()

        return [{
            "id":tag["id"],
            "tag":tag ["tag"]
        } for tag in tags] if tags else None

    def get_lyric_tags_with_query(self,query):
        query = f"%{query}%"
        tags = self.db.execute(text("""
        SELECT id,tag FROM lyric_tags 
        WHERE tag LIKE :query
        ORDER BY id
        """),{"query":query}).fetchall()

        return [{
            "id":tag["id"],
            "tag":tag["tag"]
        } for tag in tags] if tags else None