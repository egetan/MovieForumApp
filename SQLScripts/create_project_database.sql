-- First, create a database.
-- Second, connect to that database, open a query console and execute all below.

CREATE TYPE name AS
(
  fname varchar(50),
  mname varchar(50),
  lname varchar(50)
);

CREATE TYPE address AS
(
  country varchar,
  province varchar,
  district varchar,
  street varchar,
  apartment varchar
);

CREATE TYPE numeric_rating AS
 ENUM ('1','2','3','4','5');

 CREATE TYPE verbal_rating AS
 ENUM ('terrible','bad','normal','good','excellent');


CREATE TABLE genre (
	name varchar(50) NOT NULL,
	movie_id_movie integer NOT NULL,
	CONSTRAINT genre_pk PRIMARY KEY (name)

);

create table artist
(
    name          name       not null,
    artist_id     integer generated always as identity
        constraint artist_pk
            primary key,
    gender        varchar(6) not null,
    date_of_birth date       not null,
    age numeric GENERATED ALWAYS AS (2020 - date_part('year', date_of_birth)) STORED
);

CREATE FUNCTION compute_age() RETURNS trigger AS $compute_age$
    BEGIN
        NEW.age = date_part('year', now()) - date_part('year', NEW.date_of_birth);
        RETURN NEW;
    END;
$compute_age$ LANGUAGE plpgsql;

CREATE TRIGGER compute_age AFTER INSERT ON artist
    FOR EACH ROW EXECUTE FUNCTION compute_age();

CREATE TABLE actor (
	CONSTRAINT actor_pk PRIMARY KEY (artist_id)
)
 INHERITS(artist);

CREATE TABLE director (
	CONSTRAINT director_pk PRIMARY KEY (artist_id)
)
 INHERITS(artist);

CREATE TABLE producer (
	CONSTRAINT producer_pk PRIMARY KEY (artist_id)
)
 INHERITS(artist);

CREATE TABLE "user" (
	user_id integer NOT NULL GENERATED ALWAYS AS IDENTITY ,
	username varchar(50) NOT NULL,
	password varchar(50) NOT NULL,
	email varchar(100),
	address address,
	phone varchar,
	name name NOT NULL,
	CONSTRAINT user_pk PRIMARY KEY (user_id)

);

CREATE TABLE rating (
	numeric_rating numeric_rating,
	verbal_rating verbal_rating,
	movie_id integer,
	user_id_user integer NOT NULL
);

CREATE TABLE comment (
	comment_id integer NOT NULL GENERATED ALWAYS AS IDENTITY ,
	content varchar NOT NULL,
	number_of_likes integer NOT NULL DEFAULT 0,
	number_of_dislikes integer NOT NULL DEFAULT 0,
	movie_id integer,
	user_id_user integer NOT NULL,
	CONSTRAINT comment_pk PRIMARY KEY (comment_id)

);

CREATE TABLE movie (
	movie_id integer NOT NULL GENERATED ALWAYS AS IDENTITY ,
	date_of_release date NOT NULL,
	title varchar(100) NOT NULL,
	average_rating float,
	budget bigint,
	income bigint,
	revenue bigint,
	CONSTRAINT movie_pk PRIMARY KEY (movie_id)

);

ALTER TABLE genre ADD CONSTRAINT movie_fk FOREIGN KEY (movie_id_movie)
REFERENCES movie (movie_id) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;

CREATE TABLE many_actor_acts_in_many_movies (
	movie_id_movie integer NOT NULL,
	artist_id_actor integer NOT NULL,
	CONSTRAINT many_actor_acts_in_many_movies_pk PRIMARY KEY (movie_id_movie,artist_id_actor)

);

ALTER TABLE many_actor_acts_in_many_movies ADD CONSTRAINT movie_fk FOREIGN KEY (movie_id_movie)
REFERENCES movie (movie_id) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;

ALTER TABLE many_actor_acts_in_many_movies ADD CONSTRAINT actor_fk FOREIGN KEY (artist_id_actor)
REFERENCES actor (artist_id) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;

CREATE TABLE many_movie_has_many_director (
	movie_id_movie integer NOT NULL,
	artist_id_director integer NOT NULL,
	CONSTRAINT many_movie_has_many_director_pk PRIMARY KEY (movie_id_movie,artist_id_director)

);

ALTER TABLE many_movie_has_many_director ADD CONSTRAINT movie_fk FOREIGN KEY (movie_id_movie)
REFERENCES movie (movie_id) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;

ALTER TABLE many_movie_has_many_director ADD CONSTRAINT director_fk FOREIGN KEY (artist_id_director)
REFERENCES director (artist_id) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;

CREATE TABLE many_movie_has_many_producer (
	movie_id_movie integer NOT NULL,
	artist_id_producer integer NOT NULL,
	CONSTRAINT many_movie_has_many_producer_pk PRIMARY KEY (movie_id_movie,artist_id_producer)

);

ALTER TABLE many_movie_has_many_producer ADD CONSTRAINT movie_fk FOREIGN KEY (movie_id_movie)
REFERENCES movie (movie_id) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;

ALTER TABLE many_movie_has_many_producer ADD CONSTRAINT producer_fk FOREIGN KEY (artist_id_producer)
REFERENCES producer (artist_id) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;

ALTER TABLE rating ADD CONSTRAINT user_fk FOREIGN KEY (user_id_user)
REFERENCES "user" (user_id) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;

ALTER TABLE comment ADD CONSTRAINT user_fk FOREIGN KEY (user_id_user)
REFERENCES "user" (user_id) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;

CREATE TABLE reply (
	reply_id integer NOT NULL GENERATED ALWAYS AS IDENTITY ,
	content varchar NOT NULL,
	parent_reply_id integer,
	comment_id_comment integer NOT NULL,
	CONSTRAINT reply_pk PRIMARY KEY (reply_id)

);

ALTER TABLE reply ADD CONSTRAINT comment_fk FOREIGN KEY (comment_id_comment)
REFERENCES comment (comment_id) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;

ALTER TABLE reply ADD CONSTRAINT reply_uq UNIQUE (comment_id_comment);

ALTER TABLE rating ADD CONSTRAINT rated_movie_fk FOREIGN KEY (movie_id)
REFERENCES movie (movie_id) MATCH FULL
ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE comment ADD CONSTRAINT movie_fk FOREIGN KEY (movie_id)
REFERENCES movie (movie_id) MATCH FULL
ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE reply ADD CONSTRAINT parent_reply_id_fk FOREIGN KEY (parent_reply_id)
REFERENCES reply (reply_id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION;
