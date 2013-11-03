BEGIN TRANSACTION;

DROP TABLE IF EXISTS users;
CREATE TABLE users(
	id INTEGER,
	email TEXT,
	session_id TEXT,
    timestamp DATETIME DEFAULT (datetime('now','localtime')),
	password TEXT,
	PRIMARY KEY(id)
);

DROP TABLE IF EXISTS locations;
CREATE TABLE locations(
	user_id INTEGER,
	lng REAL,
	lat REAL,
    timestamp DATETIME DEFAULT (datetime('now','localtime')),
	duration INTEGER,
	PRIMARY KEY(user_id, lng, lat, timestamp),
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

INSERT INTO users(email, password) VALUES('user@test.com', 'pass');

COMMIT;

