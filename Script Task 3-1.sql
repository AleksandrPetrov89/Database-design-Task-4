psql -U postgres -d postgres
CREATE USER netology_task WITH PASSWORD '1234';
CREATE DATABASE task_1 WITH OWNER netology_task;
\q
psql -U netology_task -d task_1

CREATE TABLE IF NOT EXISTS genres (
	id SERIAL PRIMARY KEY,
	title VARCHAR(60) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS artists (
	id SERIAL PRIMARY KEY,
	name VARCHAR(60) NOT NULL,
	alias VARCHAR(40) UNIQUE
);

CREATE TABLE IF NOT EXISTS genresartists (
	genresid INTEGER REFERENCES genres(id),
	artistsid INTEGER REFERENCES artists(id),
	CONSTRAINT pkgenresartists PRIMARY KEY (genresid, artistsid)
);

CREATE TABLE IF NOT EXISTS albums (
	id SERIAL PRIMARY KEY,
	title VARCHAR(100) NOT NULL,
	releaseyear INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS artistsalbums (
	artistsid INTEGER REFERENCES artists(id),
	albumsid INTEGER REFERENCES albums(id),
	CONSTRAINT pkartistsalbums PRIMARY KEY (artistsid, albumsid)
);

CREATE TABLE IF NOT EXISTS musicalcompositions (
	id SERIAL PRIMARY KEY,
	albumsid INTEGER NOT NULL REFERENCES albums(id),
	title VARCHAR(100) NOT NULL,
	duration INTERVAL SECOND NOT NULL
);

CREATE TABLE IF NOT EXISTS musiccollections (
	id SERIAL PRIMARY KEY,
	title VARCHAR(100) NOT NULL,
	releaseyear INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS collectionscompositions (
	compositionsid INTEGER REFERENCES musicalcompositions(id),
	collectionsid INTEGER REFERENCES musiccollections(id),
	CONSTRAINT pkcollectionscompositions PRIMARY KEY (compositionsid, collectionsid)
);
