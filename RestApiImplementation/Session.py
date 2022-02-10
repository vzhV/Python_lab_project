from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask import Blueprint
sesion = Blueprint("sesion",__name__)
some_engine = create_engine('mysql+pymysql://root:zh683099@localhost/pplab7')
some_engine.connect()
Session = sessionmaker(bind=some_engine)

session = Session()
"""
User1 = User(nickname = 'baka', firstname = 'Ellen', lastname = 'Smith', email = 'winchester2017@gmail.com', password = 'winchester2017')
Song1 = Song(name = 'Collide', singer = 'Ed Sheeran', duration = '3:30')
Playlist1 = Playlist(name = 'Loft', is_private = True, user_id = 1)
Playlist_song = Songs_playlist(song_id = 1, playlist_id = 1)
session.add(User1)
session.add(Song1)
session.add(Playlist1)
session.add(Playlist_song)
session.commit()
"""
