class LyricTagService:
    def __init__(self,lyric_tag_dao):
        self.dao = lyric_tag_dao


    def create_new_lyric_tag(self,tag_name):
        new_lyric_tag_id = self.dao.insert_lyric_tag(tag_name)
        return new_lyric_tag_id

    def create_new_map(self,tag_id,song_id):
        check = self.dao.insert_map(tag_id,song_id)
        return check

    def song_list_of_lyric_tag(self,lyric_tag_id):
        song_list = self.dao.get_song_list_of_lyric_tag(lyric_tag_id)
        return song_list

    def lyric_tags_of_song(self,song_id):
        tags = self.dao.get_lyric_tags_of_song(song_id)
        return tags

    def lyric_tags_with_query(self,query):
        return self.dao.get_lyric_tags_with_query(query)
