import pytest
import config
import json

from app import create_app
from sqlalchemy import text, create_engine

database = create_engine(config.test_config["DB_URL"],encoding='utf-8',max_overflow=0)

@pytest.fixture
def api():
    app = create_app(config.test_config)
    app.config["TEST"] = True
    api = app.test_client()
    
    return api

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
        {'id':2,'title':'dragon2',"artist":"fire","e_label":2,"v_label":2,"mood_tag":'chill'},
        {'id':3,'title':'dragon3',"artist":"dragon","e_label":1,"v_label":2,"mood_tag":'평안한'}

    ]
    database.execute(text("""
    INSERT INTO songs (id,title,artist,e_label,v_label,mood_tag)
    VALUES (:id,:title,:artist,:e_label,:v_label,:mood_tag)
    """),new_songs)

    new_lyric_tags = [{"id":1,"tag":"운동"},{"id":2,"tag":"운동광"},{"id":3,"tag":"드라이브"}]
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

def test_ping(api):
    res = api.get('/ping')
    assert b'pong' in res.data

def test_search_song(api):
    query = 'dragon'
    res = api.get(f'/song/{query}')
    assert res.status_code ==200
    songs = json.loads(res.data.decode('utf-8'))
    assert songs["songs"][0]["title"] == "dragon1" and len(songs["songs"]) ==3

def test_mood_tag_basis_search(api):
    query = "cool"
    res = api.get(f'/song/moodtag/{query}')
    assert res.status_code==200
    songs = json.loads(res.data.decode('utf-8'))
    assert songs["songs"][0]["artist"] == 'dragon' and len(songs["songs"]) ==1

def test_lyric_tag_basis_search(api):
    #"운동" 테그로 검색
    target_tag_id = 1
    res = api.get(f'/song/lyrictag/{target_tag_id}')
    assert res.status_code ==200
    songs = json.loads(res.data.decode('utf-8'))
    assert len(songs["songs"])==2 and songs["songs"][0]["artist"] == 'dragon' and songs["songs"][1]["artist"] == 'fire'

def test_mood_tag(api):
    res = api.get('/moodtag')
    assert res.status_code ==200
    mood_tags = json.loads(res.data.decode('utf-8'))
    assert len(mood_tags["mood_tags"]) ==3

def test_lyrictag_of_song(api):
    test_song_id = 1
    res = api.get(f'/lyrictag/song/{test_song_id}')
    assert res.status_code ==200
    lyrictags = json.loads(res.data.decode('utf-8'))
    assert len(lyrictags["lyric_tags"]) ==2

def test_search_lyrictag_with_query(api):
    #운동 으로 검색하면 "운동" 태그랑 "운동광" 태그를 반환해야한다.
    query = "운동"
    res = api.get(f'/lyrictag/{query}')
    assert res.status_code ==200
    lyrictags = json.loads(res.data.decode('utf-8'))
    assert len(lyrictags["lyric_tags"]) ==2 and lyrictags["lyric_tags"][0]["tag"] == "운동"\
        and lyrictags["lyric_tags"][1]["tag"] == "운동광"

def test_create_song(api):
    res = api.post('/create/song', data=json.dumps({'title':'dragon4',"artist":"dragon","e_label":1,"v_label":2,"mood_tag":'평안한'}),
    content_type = 'application/json')
    assert res.status_code == 200
    query = 'dragon4'
    res = api.get(f'/song/{query}')
    assert res.status_code ==200

def test_create_lyric_tag(api):
    res = api.post('/create/lyrictag',data=json.dumps({'tag_name':'test_tag'}), content_type='application/json')
    assert res.status_code ==200

def test_create_map(api):
    res = api.post('/create/map',data=json.dumps({'song_id':1,'tag_id':3}),content_type='application/json')
    assert res.status_code== 200



