from flask import jsonify,request,Response


def create_endpoints(app,services):
    song_service = services.song_service
    lyric_tag_service = services.lyric_tag_service

    #ping test
    @app.route('/ping', methods=["GET"])
    def ping():
        return "pong"

    ##song 검색창에 검색했을때 query에 맞는 노래 모두 반환
    @app.route('/song/<query>',methods=["GET"])
    def song(query):
        songs = song_service.song_list(query)
        return jsonify({
            "songs":songs
        })
    #mood tag 클릭 했을때 해당 곡들 반환
    @app.route('/song/moodtag/<query>',methods=["GET"])
    def mood_tag_song_list(query):
        songs = song_service.song_list_with_mood_tag(query)
        return jsonify({
            "songs":songs
        })
    #lyrics tag를 눌렀을때 해당 곡들을 반환
    @app.route('/song/lyrictag/<int:tag_id>',methods=['GET'])
    def lyrictag_songs(tag_id):
        songs = lyric_tag_service.song_list_of_lyric_tag(tag_id)
        return jsonify({
            "songs":songs
        })
    #mood tag들 반환
    @app.route('/moodtag',methods=["GET"])
    def mood_tag():
        tags = song_service.mood_tags()
        return jsonify({
            "mood_tags":tags
        })

    #song list 클라이언트단에서 각 곡의 가사기반 태그듧 반환
    @app.route('/lyrictag/song/<int:song_id>', methods=["GET"])
    def lyrictag_of_song(song_id):
        lyric_tags = lyric_tag_service.lyric_tags_of_song(song_id)
        return jsonify({
            "lyric_tags":lyric_tags
        })
    #검색창에 lyric태그 기반으로 검색 했을때 lyric태그 들을 반환
    @app.route('/lyrictag/<query>',methods=["GET"])
    def search_lyrictag(query):
        tags = lyric_tag_service. lyric_tags_with_query(query)
        return jsonify({
            "lyric_tags":tags
        })
    @app.route('/create/song',methods=["POST"])
    def create_song():
        new_song = request.json
        new_song_id = song_service.create_new_song(new_song)
        if new_song_id:
            return '',200
        return 'failed', 404

    @app.route('/create/lyrictag',methods=["POST"])
    def create_lyrictag():
        new_tag = request.json
        new_tag_name = new_tag["tag_name"]
        new_tag_id = lyric_tag_service.create_new_lyric_tag(new_tag_name)
        if new_tag_id:
            return '',200
        return 'failed', 404
    @app.route('/create/map',methods=["POST"])
    def create_map():
        payload = request.json
        new_map_tag_id = payload['tag_id']
        new_map_song_id = payload['song_id']
        check = lyric_tag_service.create_new_map(new_map_tag_id,new_map_song_id)
        if check:
            return '',200
        return 'failed',404





