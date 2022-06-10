import sqlalchemy
from random import randint
from pprint import pprint


def populating_database():
    artists = [{'name': "'Ро́бин Риа́нна Фе́нти'", 'alias': "'Риа́нна'"},
               {'name': "'Зарифа́ Паша́евна Мгоя́н'", 'alias': "'За́ра'"},
               {'name': "'Ната́лья Ильи́нична Чистяко́ва-Ио́нова'", 'alias': "'Глюко́за'"},
               {'name': "'Александр Валерьевич Фадеев'", 'alias': "'Данко'"},
               {'name': "'Елизаве́та Вальдема́ровна Иванци́в'", 'alias': "'Ёлка'"},
               {'name': "'Александр Александрович Бреславский'", 'alias': "'Доминик Джокер'"},
               {'name': "'Са́ра Льво́вна Манахи́мова'", 'alias': "'Жасми́н'"},
               {'name': "'Его́р Никола́евич Була́ткин'", 'alias': "'Его́р Крид'"},
               {'name': "'Игорь Анатольевич Сорокин'", 'alias': "'Игорёк'"}]

    for artist in artists:
        request = f"INSERT INTO artists(name, alias)\n"\
                  f"VALUES({artist['name']}, {artist['alias']});"
        connection.execute(request)

    genres = ["'поп'", "'электропоп'", "'синтипоп'", "'трэп'", "'современный R&B'",
              "'альтернативный рок'", "'русский рок'", "'хип-хоп'", "'поп-рок'"]

    for genre in genres:
        request = f"INSERT INTO genres(title)\n" \
                  f"VALUES({genre});"
        connection.execute(request)

    albums = ["'Свистки и бумажки'", "'Психи попадают в топ'", "'Выход в город'",
              "'Радио Апокалипсис'", "'Красота и уродство'", "'Княжна из хрущевки'",
              "'Pussy Boy'", "'Не важно, что говорят кисы'", "'Красный закат'",
              "'Мои (твои) темные желания'", "'Контроль'", "'Зеркало'"]

    for count, album in enumerate(albums):
        if count < 3:
            year_1 = 2017
        elif count < 6:
            year_1 = 2018
        elif count < 9:
            year_1 = 2019
        else:
            year_1 = 2020
        request = f"INSERT INTO albums(title, releaseyear)\n" \
                  f"VALUES({album}, {year_1});"
        connection.execute(request)

    music_tracks = ["'Титры'", "'Отпускаю'", "'Бывшие'", "'Лампочки'", "'Никто'", "'Двое бывших'",
                    "'Полюбил тебя'", "'По другому'", "'Как я захочу'", "'Гармония'", "'Среди бывших'",
                    "'По душам'", "'Если в сердце живёт любовь'", "'Седьмой Лепесток'", "'Хочешь'",
                    "'Пташка'", "'Мой костёр'", "'Родной мой'", "'Мой мир сошёл с ума'", "'Мой гитарист'"]

    for count, track in enumerate(music_tracks, start=1):
        if count <= len(albums):
            albums_id = count
        else:
            albums_id = randint(1, len(albums))
        request = f"INSERT INTO musicalcompositions(albumsid, title, duration)\n" \
                  f"VALUES({albums_id}, {track}, '{randint(150, 360)}');"
        connection.execute(request)

    for music_collection in range(1, 9):
        title = f"'Сборник № {music_collection}'"
        releas_eyear = randint(2015, 2022)
        request = f"INSERT INTO musiccollections(title, releaseyear)\n" \
                  f"VALUES({title}, {releas_eyear});"
        connection.execute(request)

    artists_id = connection.execute("SELECT id FROM artists;").fetchall()
    for artist in artists_id:
        genres_id = connection.execute("SELECT id FROM genres;").fetchall()
        for number_genres in range(1, randint(3, 5)):
            i = randint(0, len(genres_id)-1)
            genre = str(genres_id.pop(i))[1:-2]
            request = f"INSERT INTO genresartists(genresid, artistsid)\n" \
                      f"VALUES({genre}, {str(artist)[1:-2]});"
            connection.execute(request)

        albums_id = connection.execute("SELECT id FROM albums;").fetchall()
        for number_albums in range(1, randint(4, 6)):
            i = randint(0, len(albums_id) - 1)
            album = str(albums_id.pop(i))[1:-2]
            request = f"INSERT INTO artistsalbums(artistsid, albumsid)\n" \
                      f"VALUES({str(artist)[1:-2]}, {album});"
            connection.execute(request)

    music_collections_id = connection.execute("SELECT id FROM musiccollections;").fetchall()
    for music_collection in music_collections_id:
        tracks_id = connection.execute("SELECT id FROM musicalcompositions;").fetchall()
        for count in range(10):
            i = randint(0, len(tracks_id) - 1)
            track = str(tracks_id.pop(i))[1:-2]
            request = f"INSERT INTO collectionscompositions(compositionsid, collectionsid)\n" \
                      f"VALUES({track}, {str(music_collection)[1:-2]});"
            connection.execute(request)


if __name__ == '__main__':
    db = 'postgresql+psycopg2://netology_task:1234@localhost:5432/task_1'
    engine = sqlalchemy.create_engine(db)
    connection = engine.connect()

    populating_database()

    year = 2018
    sql_request = f"SELECT title, releaseyear FROM albums\n" \
                  f"WHERE releaseyear = {year};"
    result = connection.execute(sql_request).fetchall()
    print("Название и год выхода альбомов, вышедших в 2018 году:")
    pprint(result)

    sql_request = f"SELECT title, duration FROM musicalcompositions\n" \
                  f"ORDER BY duration DESC\n" \
                  f"LIMIT 1;"
    result = connection.execute(sql_request).fetchall()
    print("\nНазвание и продолжительность самого длительного трека:")
    pprint(result)

    sql_request = f"SELECT title FROM musicalcompositions\n" \
                  f"WHERE duration >= '210'::interval;"
    result = connection.execute(sql_request).fetchall()
    print("\nНазвание треков, продолжительность которых не менее 3,5 минуты:")
    pprint(result)

    sql_request = f"SELECT title FROM musiccollections\n" \
                  f"WHERE releaseyear BETWEEN 2018 AND 2020;"
    result = connection.execute(sql_request).fetchall()
    print("\nНазвания сборников, вышедших в период с 2018 по 2020 год включительно:")
    pprint(result)

    sql_request = f"SELECT alias FROM artists\n" \
                  f"WHERE alias NOT LIKE '%% %%';"
    result = connection.execute(sql_request).fetchall()
    print("\nИсполнители, чье имя состоит из 1 слова:")
    pprint(result)

    sql_request = f"SELECT title FROM musicalcompositions\n" \
                  f"WHERE title ILIKE '%%мой%%' OR title ILIKE '%%my%%';"
    result = connection.execute(sql_request).fetchall()
    print("\nНазвание треков, которые содержат слово 'мой'/'my':")
    pprint(result)
