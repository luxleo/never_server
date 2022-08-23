CREATE DATABASE never;
USE never;

CREATE TABLE songs (
    id INT NOT NULL AUTO_INCREMENT,
    title VARCHAR(50) NOT NULL,
    artist VARCHAR(50) NOT NULL,
    e_label INT,
    v_label INT,
    mood_tag VARCHAR(50),
    PRIMARY KEY (id),
);

CREATE TABLE lyric_tags (
    id INT NOT NULL AUTO_INCREMENT,
    tag VARCHAR(50) NOT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY tag (tag)
);

CREATE TABLE song_lyric_tag (
    song_id INT NOT NULL,
    tag_id INT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY pk (song_id,tag_id),
    CONSTRAINT song_map_fk FOREIGN KEY (song_id) REFERENCES songs(id),
    CONSTRAINT lyric_map_fk FOREIGN KEY (tag_id) REFERENCES lyric_tags(id)
);
