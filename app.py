from flask import Flask
from sqlalchemy import create_engine
from flask_cors import CORS


from model import LyricTagDao,SongDao
from service import LyricTagService,SongService
from view import create_endpoints

class Services:
    pass
def create_app(test_config=None):
    app = Flask(__name__)

    CORS(app)

    if test_config is None:
        app.config.from_pyfile('config.py')
    else:
        app.config.update(test_config)
    
    database = create_engine(app.config["DB_URL"],encoding='utf-8',max_overflow=0)

    #Persistence layer
    song_dao = SongDao(database)
    lyric_tag_dao = LyricTagDao(database)

    #Bussiness Layer
    services = Services
    services.song_service = SongService(song_dao)
    services.lyric_tag_service = LyricTagService(lyric_tag_dao)

    #create endpoints
    create_endpoints(app,services)

    return app

