import pytest

from model import SongDao,LyricTagDao
from sqlalchemy import create_engine,text
import config

database = create_engine(config.test_config["DB_URL"],encoding='utf-8',max_overflow=0)

@pytest.fixture
def song_dao():
    return SongDao(database)

@pytest.fixture
def lyric_tag_dao():
    return LyricTagDao(database)

def setup_function():
    ###더미 유져, 태그, 맵 테이블 엔티티 생성
    new_songs = [
        {
            "id":1,
            "title":"dragon1",
            "artist":"dragon",
            "e_label":3,
            "v_label":2,
            "mood_tag":"cool"
        },

    ]
    database.execute(text("""
    INSERT INTO songs (id,title,artist,e_label,v_label,mood_tag)
    VALUES (:id,:title,:artist,:e_label,:v_label,:mood_tag)
    """),new_songs)

    new_lyric_tags = [{"id":1,"tag":"운동"}]
    database.execute(text("""
    INSERT INTO lyric_tags (id, tag) VALUES (:id, :tag)
    """),new_lyric_tags)

    new_maps = [{"song_id":1, "tag_id":1} ]
    database.execute(text("""
    INSERT INTO song_lyric_tag (song_id, tag_id) VALUES (:song_id, :tag_id)
    """), new_maps)

def teardown_function():
    database.execute(text("SET FOREIGN_KEY_CHECKS=0"))
    database.execute(text("TRUNCATE songs"))
    database.execute(text("TRUNCATE lyric_tags"))
    database.execute(text("TRUNCATE song_lyric_tag"))
    database.execute(text("SET FOREIGN_KEY_CHECKS=1"))

def get_song(song_id):
    return database.execute(text("""
    SELECT * FROM songs WHERE id = :song_id
    """),{"song_id":song_id}).fetchone()
######song dao test section
def test_insert_song(song_dao):
    new_song = {'title':'dragon2',"artist":"dragon","e_label":1,"v_label":2,"mood_tag":'chill'}
    new_song_id = song_dao.insert_song(new_song)

    song = get_song(new_song_id)
    assert song["title"] == new_song["title"]

def test_get_song_list(song_dao):
    new_song = {'title':'dragon2',"artist":"dragon","e_label":2,"v_label":2,"mood_tag":'chill'}
    new_song_id =song_dao.insert_song(new_song)
    song = song_dao.get_song_list("dragon")

    assert song[0]["title"] == "dragon1" and song[1]["title"] == "dragon2"

def test_get_song_list_with_mood_tag(song_dao):
    new_song = {'title':'dragon2',"artist":"dragon","e_label":3,"v_label":2,"mood_tag":'cool'}
    new_song_id = song_dao.insert_song(new_song)

    songs = song_dao.get_song_list_with_mood_tag('cool')
    assert len(songs) ==2

def test_get_mood_tags(song_dao):
    new_song = {'title':'dragon2',"artist":"dragon","e_label":2,"v_label":2,"mood_tag":'chill'}
    new_song_id = song_dao.insert_song(new_song)

    tags = song_dao.get_mood_tags()
    assert tags[0]["tag"] == 'cool' and tags[1]["tag"] == "chill"

#####lyric tag test section
def test_insert_lyric_tag(lyric_tag_dao):
    new_lyric_tag_id = lyric_tag_dao.insert_lyric_tag('공부')
    assert new_lyric_tag_id ==2

def test_insert_map(lyric_tag_dao,song_dao):
    new_song = {'title':'dragon2',"artist":"dragon","e_label":2,"v_label":2,"mood_tag":'chill'}
    
    new_song_id = song_dao.insert_song(new_song)
    new_lyric_tag_id = lyric_tag_dao.insert_lyric_tag('공부')

    assert new_song_id ==2 and new_lyric_tag_id ==2
    check = lyric_tag_dao.insert_map(new_lyric_tag_id,new_song_id)
    assert check

def test_get_song_list_of_lyric_tag(lyric_tag_dao,song_dao):
    new_song = {'title':'dragon2',"artist":"dragon","e_label":2,"v_label":2,"mood_tag":'chill'}
    
    new_song_id = song_dao.insert_song(new_song)
    new_lyric_tag_id = lyric_tag_dao.insert_lyric_tag('공부')

    assert new_song_id ==2 and new_lyric_tag_id ==2
    check = lyric_tag_dao.insert_map(new_lyric_tag_id,new_song_id)
    check1 = lyric_tag_dao.insert_map(new_lyric_tag_id,1)
    assert check and check1

    songs = lyric_tag_dao.get_song_list_of_lyric_tag(new_lyric_tag_id)
    assert len(songs) ==2
    assert songs[0]["title"] == "dragon1" and songs[1]["title"] == 'dragon2'

def test_get_lyric_tags_of_song(lyric_tag_dao):
    new_lyric_tag_id = lyric_tag_dao.insert_lyric_tag('공부')
    assert new_lyric_tag_id ==2
    check =lyric_tag_dao.insert_map(new_lyric_tag_id,1)
    assert check

    tags = lyric_tag_dao.get_lyric_tags_of_song(1)
    assert tags[0]["tag"] =='운동' and tags[1]["tag"] == '공부'

def test_get_lyric_tags_with_query(lyric_tag_dao):
    new_lyric_tag_id = lyric_tag_dao.insert_lyric_tag('운동광')
    assert new_lyric_tag_id ==2
    tags = lyric_tag_dao.get_lyric_tags_with_query('운동')
    assert tags[1]["tag"] == '운동광'



