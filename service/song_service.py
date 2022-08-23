class SongService:
    def __init__(self,song_dao):
        self.song_dao = song_dao

    def create_new_song(self,new_song):
        new_song_id = self.song_dao.insert_song(new_song)
        return new_song_id

    def song_list(self,query):
        return self.song_dao.get_song_list(query)

    def song_list_with_mood_tag(self,query):
        return self.song_dao.get_song_list_with_mood_tag(query)

    def mood_tags(self):
        return self.song_dao.get_mood_tags()