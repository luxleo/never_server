import pytest

import config
from sqlalchemy import create_engine,text

from model import SongDao,LyricTagDao
from service import SongService,LyricTagService

database = create_engine(config.test_config["DB_URL"], encoding='utf-8',max_overflow=0)

@pytest.fixture
def song_service():
    return SongService(SongDao(database))

@pytest.fixture
def lyric_tag_service():
    return LyricTagService(LyricTagDao(database))

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
        {'id':2,'title':'dragon2',"artist":"dragon","e_label":2,"v_label":2,"mood_tag":'chill'},
        {'id':3,'title':'dragon3',"artist":"dragon","e_label":1,"v_label":2,"mood_tag":'평안한'}

    ]
    database.execute(text("""
    INSERT INTO songs (id,title,artist,e_label,v_label,mood_tag)
    VALUES (:id,:title,:artist,:e_label,:v_label,:mood_tag)
    """),new_songs)

    new_lyric_tags = [{"id":1,"tag":"운동"},{"id":2,"tag":"가만히"},{"id":3,"tag":"드라이브"}]
    database.execute(text("""
    INSERT INTO lyric_tags (id, tag) VALUES (:id, :tag)
    """),new_lyric_tags)

    new_maps = [{"song_id":1, "tag_id":1},{"song_id":1,"tag_id":2},
    {"song_id":2, "tag_id":1},{"song_id":2,"tag_id":3},
    {"song_id":3, "tag_id":2},{"song_id":3,"tag_id":3}
    ]
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
    target_song = database.execute(text("""
    SELECT * FROM songs WHERE id =:id
    """),{"id":song_id}).fetchone()
    
    return target_song
def get_lyric_tag(tag_id):
    return database.execute(text("""
    SELECT * FROM lyric_tags WHERE id = :tag_id
    """),{"tag_id":tag_id}).fetchone()
#####test song service
def test_create_new_song(song_service):
    new_song = {'title':'dragon2',"artist":"dragon","e_label":2,"v_label":2,"mood_tag":'chill'}
    new_song_id = song_service.create_new_song(new_song)  
    assert new_song_id ==4
    new_song = get_song(new_song_id)
    assert new_song["title"] == 'dragon2'

def test_song_list(song_service):
    new_song = {'title':'dragon2',"artist":"dragon","e_label":2,"v_label":2,"mood_tag":'chill'}
    new_song_id = song_service.create_new_song(new_song)  
    assert new_song_id ==4   
    songs = song_service.song_list('dragon')
    assert songs[0]["title"] == "dragon1" and songs[3]["title"] == 'dragon2' and songs[3]["e_label"] ==2

def test_song_list_with_mood_tag(song_service):
    new_song = {'title':'dragon2',"artist":"dragon","e_label":3,"v_label":2,"mood_tag":'cool'}
    new_song_id = song_service.create_new_song(new_song)  
    assert new_song_id ==4

    songs = song_service.song_list_with_mood_tag('cool')
    assert len(songs) ==2 and songs[0]["title"] =="dragon1" and songs[1]["title"] == "dragon2"

def test_mood_tags(song_service):
    new_song = {'title':'dragon2',"artist":"dragon","e_label":2,"v_label":2,"mood_tag":'chill'}
    new_song_id = song_service.create_new_song(new_song)  
    assert new_song_id ==4  

    new_song = {'title':'dragon2',"artist":"dragon","e_label":1,"v_label":2,"mood_tag":'평안한'}
    new_song_id = song_service.create_new_song(new_song)  
    assert new_song_id ==5  

    tags = song_service.mood_tags()
    assert len(tags)==3 and tags[0]["tag"] =="cool" and tags[1]["tag"] == 'chill' and tags[2]["tag"] == "평안한"

def test_create_new_lyric_tag(lyric_tag_service):
    new_tag = {"tag":"test"}
    new_tag_id = lyric_tag_service.create_new_lyric_tag(new_tag["tag"])
    target_tag = get_lyric_tag(new_tag_id)
    assert new_tag_id == 4 and target_tag["tag"] == "test"

def test_create_new_map(lyric_tag_service):
    new_map = {"song_id":1,"tag_id":3}
    check =lyric_tag_service.create_new_map(new_map["tag_id"],new_map["song_id"])
    
    assert check

def test_song_list_of_lyric_tag(lyric_tag_service):
    songs = lyric_tag_service.song_list_of_lyric_tag(1)
    assert len(songs) ==2 and songs[0]["title"] == "dragon1" and songs[1]["title"] == 'dragon2'

def test_lyric_tags_of_song(lyric_tag_service):
    test_song_id = 1
    tags = lyric_tag_service.lyric_tags_of_song(test_song_id)

    assert len(tags) ==2 and tags[0]["tag"] == '운동' and tags[1]["tag"] =='가만히'

def test_lyric_tags_with_query(lyric_tag_service):
    new_tag = {"tag":"운동광"}
    new_tag_id = lyric_tag_service.create_new_lyric_tag(new_tag["tag"])
    assert new_tag_id == 4
    new_map = {"tag_id":new_tag_id,"song_id":1}
    check =lyric_tag_service.create_new_map(new_map["tag_id"],new_map["song_id"])
    assert check 

    tags = lyric_tag_service.lyric_tags_with_query('운동')
    assert len(tags) ==2 and tags[0]["tag"] == "운동" and tags[1]["tag"] =="운동광"
