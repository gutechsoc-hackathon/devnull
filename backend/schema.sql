BEGIN TRANSACTION;

DROP TABLE IF EXISTS users;
CREATE TABLE users(
	id INTEGER,
	email TEXT,
	session_id TEXT,
	last_access TEXT,
	password TEXT,
	PRIMARY KEY(id)
);

DROP TABLE IF EXISTS locations;
CREATE TABLE locations(
	user_id INTEGER,
	lng REAL,
	lat REAL,
	time TEXT,
	duration INTEGER,
	PRIMARY KEY(user_id, lng, lat, time),
	FOREIGN KEY(user_id) REFERENCES users(id)
);
DROP TABLE IF EXISTS visited_venues;
CREATE TABLE visited_venues(
	user_id INTEGER,
	foursquare_id TEXT,
	weather_type_id INTEGER,
	duration INTEGER,
	PRIMARY KEY(user_id, foursquare_id),
	FOREIGN KEY(user_id) REFERENCES users(id)
);

COMMIT;
