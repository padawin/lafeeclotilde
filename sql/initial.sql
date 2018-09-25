BEGIN;
DROP TABLE IF EXISTS picture;
CREATE TABLE picture (
	id_picture SERIAL PRIMARY KEY,
	file_name VARCHAR(255) NOT NULL,
	hash VARCHAR(40) NOT NULL DEFAULT '',
	exif JSONB NOT NULL DEFAULT '{}'::jsonb,
	date_created TIMESTAMP WITH TIME ZONE DEFAULT 'NOW()'
);

DROP TABLE IF EXISTS category;
CREATE TABLE category (
	id_category SERIAL PRIMARY KEY,
	name VARCHAR(255) UNIQUE NOT NULL,
	date_created TIMESTAMP WITH TIME ZONE DEFAULT 'NOW()'
);


DROP TABLE IF EXISTS picture_category;
CREATE TABLE picture_category (
	id_picture_category SERIAL PRIMARY KEY,
	id_picture INT REFERENCES picture(id_picture),
	id_category INT REFERENCES category(id_category),
	date_created TIMESTAMP WITH TIME ZONE DEFAULT 'NOW()'
);
COMMIT;
