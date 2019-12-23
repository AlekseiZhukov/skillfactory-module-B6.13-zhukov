import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


DB_PATH = "sqlite:///albums.sqlite3"
Base = declarative_base()

class Error(Exception):
    pass


class AlreadyExists(Error):
    pass


class Album(Base):
    """
    Описывает структуру таблицы album для хранения записей музыкальной библиотеки
    """

    __tablename__ = "album"

    id = sa.Column(sa.INTEGER, primary_key=True)
    year = sa.Column(sa.INTEGER)
    artist = sa.Column(sa.TEXT)
    genre = sa.Column(sa.TEXT)
    album = sa.Column(sa.TEXT)


def connect_db():
    """
    Устанавливает соединение к базе данных, создает таблицы, если их еще нет и возвращает объект сессии 
    """
    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()


def find(artist):
    """
    Находит все альбомы в базе данных по заданному артисту
    """
    session = connect_db()
    albums = session.query(Album).filter(Album.artist == artist).all()
    albums_cnt = session.query(Album).filter(Album.artist == artist).count()
    return albums, albums_cnt

def save_album(year, artist, genre, album):
    """
    Записываем новый альбом в базу
    """
    #проверка на корректность типа указанных данных
    assert isinstance (year, int), "Не корректная дата"
    assert isinstance (artist, str), "Не корректное указание имени артиста"
    assert isinstance (genre, str), "Не корректное указания жанра"
    assert isinstance (album, str), "Не корректное указание названия альбома"
    
    session = connect_db()
    #делаем запрос к таблице Album БД  для поиска данных по имени создаваемого альбома и фильтруем 
    # данные по названию альбома и имени артиста
    saved_album = session.query(Album).filter(Album.album == album, Album.artist == artist).first()
    if saved_album is not None:
        raise AlreadyExists("Альбом записан в базу данных и имеет id #{}".format(saved_album.id))
                            
    # Создаем объект класса Album
    album = Album(
        year=year,
        artist=artist,
        genre=genre,
        album=album
    )
    
    session.add(album)
    session.commit()
    return album

    


    



