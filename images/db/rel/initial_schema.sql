CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS POSTGIS;
CREATE EXTENSION IF NOT EXISTS POSTGIS_TOPOLOGY;

CREATE TABLE public.tournaments (
	id              INTEGER PRIMARY KEY,
	name            VARCHAR(250) UNIQUE NOT NULL,
	created_on      TIMESTAMP NOT NULL DEFAULT NOW(),
	updated_on      TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE public.countries (
	id              INTEGER PRIMARY KEY,
	name            VARCHAR(250) UNIQUE NOT NULL,
	created_on      TIMESTAMP NOT NULL DEFAULT NOW(),
	updated_on      TIMESTAMP NOT NULL DEFAULT NOW()
);


CREATE TABLE public.games (
	id              INTEGER PRIMARY KEY,
	tournament_id   INTEGER NOT NULL,
	date 		  	DATE NOT NULL,
	home_team       VARCHAR(250) NOT NULL,
	away_team       VARCHAR(250) NOT NULL,
	score      		VARCHAR(250) NOT NULL,
	city      		VARCHAR(250) NOT NULL,
	geom            GEOMETRY,
	country_id      INTEGER NOT NULL,
	created_on      TIMESTAMP NOT NULL DEFAULT NOW(),
	updated_on      TIMESTAMP NOT NULL DEFAULT NOW()
);


ALTER TABLE games
    ADD CONSTRAINT games_countries_id_fk
        FOREIGN KEY (country_id) REFERENCES countries
            ON DELETE CASCADE;

ALTER TABLE games
    ADD CONSTRAINT games_tournaments_id_fk
        FOREIGN KEY (tournament_id) REFERENCES tournaments
            ON DELETE SET NULL;



