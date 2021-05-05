-- django tables.

create table django_content_type
(
    id        serial       not null
        constraint django_content_type_pkey
            primary key,
    app_label varchar(100) not null,
    model     varchar(100) not null,
    constraint django_content_type_app_label_model_76bd3d3b_uniq
        unique (app_label, model)
);

alter table django_content_type
    owner to postgres;

create table auth_permission
(
    id              serial       not null
        constraint auth_permission_pkey
            primary key,
    name            varchar(255) not null,
    content_type_id integer      not null
        constraint auth_permission_content_type_id_2f476e4b_fk_django_co
            references django_content_type
            deferrable initially deferred,
    codename        varchar(100) not null,
    constraint auth_permission_content_type_id_codename_01ab375a_uniq
        unique (content_type_id, codename)
);

alter table auth_permission
    owner to postgres;

create index auth_permission_content_type_id_2f476e4b
    on auth_permission (content_type_id);

create table auth_group
(
    id   serial       not null
        constraint auth_group_pkey
            primary key,
    name varchar(150) not null
        constraint auth_group_name_key
            unique
);

alter table auth_group
    owner to postgres;

create index auth_group_name_a6ea08ec_like
    on auth_group (name);

create table auth_group_permissions
(
    id            serial  not null
        constraint auth_group_permissions_pkey
            primary key,
    group_id      integer not null
        constraint auth_group_permissions_group_id_b120cbf9_fk_auth_group_id
            references auth_group
            deferrable initially deferred,
    permission_id integer not null
        constraint auth_group_permissio_permission_id_84c5c92e_fk_auth_perm
            references auth_permission
            deferrable initially deferred,
    constraint auth_group_permissions_group_id_permission_id_0cd325b0_uniq
        unique (group_id, permission_id)
);

alter table auth_group_permissions
    owner to postgres;

create index auth_group_permissions_group_id_b120cbf9
    on auth_group_permissions (group_id);

create index auth_group_permissions_permission_id_84c5c92e
    on auth_group_permissions (permission_id);

create table "MovieForumApp_user"
(
    id           serial                   not null
        constraint "MovieForumApp_user_pkey"
            primary key,
    password     varchar(128)             not null,
    last_login   timestamp with time zone,
    is_superuser boolean                  not null,
    username     varchar(150)             not null
        constraint "MovieForumApp_user_username_key"
            unique,
    first_name   varchar(150)             not null,
    last_name    varchar(150)             not null,
    email        varchar(254)             not null,
    is_staff     boolean                  not null,
    is_active    boolean                  not null,
    date_joined  timestamp with time zone not null,
    photo        varchar(100)             not null
);

alter table "MovieForumApp_user"
    owner to postgres;

create index "MovieForumApp_user_username_84ed5cd9_like"
    on "MovieForumApp_user" (username);

create table "MovieForumApp_user_groups"
(
    id       serial  not null
        constraint "MovieForumApp_user_groups_pkey"
            primary key,
    user_id  integer not null
        constraint "MovieForumApp_user_g_user_id_4191df74_fk_MovieForu"
            references "MovieForumApp_user"
            deferrable initially deferred,
    group_id integer not null
        constraint "MovieForumApp_user_groups_group_id_59261fa5_fk_auth_group_id"
            references auth_group
            deferrable initially deferred,
    constraint "MovieForumApp_user_groups_user_id_group_id_d800fe1a_uniq"
        unique (user_id, group_id)
);

alter table "MovieForumApp_user_groups"
    owner to postgres;

create index "MovieForumApp_user_groups_user_id_4191df74"
    on "MovieForumApp_user_groups" (user_id);

create index "MovieForumApp_user_groups_group_id_59261fa5"
    on "MovieForumApp_user_groups" (group_id);

create table "MovieForumApp_user_user_permissions"
(
    id            serial  not null
        constraint "MovieForumApp_user_user_permissions_pkey"
            primary key,
    user_id       integer not null
        constraint "MovieForumApp_user_u_user_id_ad6bc54c_fk_MovieForu"
            references "MovieForumApp_user"
            deferrable initially deferred,
    permission_id integer not null
        constraint "MovieForumApp_user_u_permission_id_427a0514_fk_auth_perm"
            references auth_permission
            deferrable initially deferred,
    constraint "MovieForumApp_user_user__user_id_permission_id_a109019e_uniq"
        unique (user_id, permission_id)
);

alter table "MovieForumApp_user_user_permissions"
    owner to postgres;

create index "MovieForumApp_user_user_permissions_user_id_ad6bc54c"
    on "MovieForumApp_user_user_permissions" (user_id);

create index "MovieForumApp_user_user_permissions_permission_id_427a0514"
    on "MovieForumApp_user_user_permissions" (permission_id);

create table "MovieForumApp_userprofile"
(
    id      serial       not null
        constraint "MovieForumApp_userprofile_pkey"
            primary key,
    photo   varchar(100) not null,
    user_id integer      not null
        constraint "MovieForumApp_userprofile_user_id_key"
            unique
        constraint "MovieForumApp_userpr_user_id_4b897c65_fk_MovieForu"
            references "MovieForumApp_user"
            on update cascade on delete cascade
            deferrable initially deferred
);

alter table "MovieForumApp_userprofile"
    owner to postgres;

create table django_admin_log
(
    id              serial                   not null
        constraint django_admin_log_pkey
            primary key,
    action_time     timestamp with time zone not null,
    object_id       text,
    object_repr     varchar(200)             not null,
    action_flag     smallint                 not null
        constraint django_admin_log_action_flag_check
            check (action_flag >= 0),
    change_message  text                     not null,
    content_type_id integer
        constraint django_admin_log_content_type_id_c4bce8eb_fk_django_co
            references django_content_type
            deferrable initially deferred,
    user_id         integer                  not null
        constraint "django_admin_log_user_id_c564eba6_fk_MovieForumApp_user_id"
            references "MovieForumApp_user"
            deferrable initially deferred
);

alter table django_admin_log
    owner to postgres;

create index django_admin_log_content_type_id_c4bce8eb
    on django_admin_log (content_type_id);

create index django_admin_log_user_id_c564eba6
    on django_admin_log (user_id);

create table django_session
(
    session_key  varchar(40)              not null
        constraint django_session_pkey
            primary key,
    session_data text                     not null,
    expire_date  timestamp with time zone not null
);

alter table django_session
    owner to postgres;

create index django_session_session_key_c0390e0f_like
    on django_session (session_key);

create index django_session_expire_date_a5c62663
    on django_session (expire_date);




-- project


CREATE TABLE movie (
	movie_id integer NOT NULL GENERATED ALWAYS AS IDENTITY ,
	date_of_release date NOT NULL,
	title varchar(100) NOT NULL,
	budget integer,
	income integer,
    trailer varchar(100),
    description text,
    image varchar(100),
    runtime int,
    plot_keywords text[],
	revenue integer generated always as ( income - budget ) STORED ,
	CONSTRAINT movie_pk PRIMARY KEY (movie_id)
);

CREATE TABLE genre (
	name varchar(50) NOT NULL,
	CONSTRAINT genre_pk PRIMARY KEY (name)

);

CREATE TABLE country
(
    country_name varchar(100) NOT NULL
        CONSTRAINT country_pk
            PRIMARY KEY
);

CREATE TABLE actor (
	actor_id integer NOT NULL GENERATED ALWAYS AS IDENTITY ,
	gender varchar(6) NOT NULL,
	fname varchar(50) NOT NULL,
	mname varchar(2),
	lname varchar(50) NOT NULL,
	date_of_birth date NOT NULL,
	image varchar(100),
	country_name varchar(100),
	description text,
	instagram varchar(100),
	twitter varchar(100),
	linkedin varchar(100),
    age numeric GENERATED ALWAYS AS (2020 - date_part('year', date_of_birth)) STORED,
	CONSTRAINT actor_pk PRIMARY KEY (actor_id)
);

ALTER TABLE actor ADD CONSTRAINT actor_country_country_name_fk FOREIGN KEY (country_name) REFERENCES  country(country_name);

CREATE TABLE director (
	director_id integer NOT NULL GENERATED ALWAYS AS IDENTITY ,
	gender varchar(6) NOT NULL,
	fname varchar(50) NOT NULL,
	mname varchar(2),
	lname varchar(50) NOT NULL,
	date_of_birth date NOT NULL,
    	image varchar(100),
    	country_name varchar(100),
	description text,
	instagram varchar(100),
	twitter varchar(100),
	linkedin varchar(100),
    age numeric GENERATED ALWAYS AS (2020 - date_part('year', date_of_birth)) STORED,
	CONSTRAINT director_pk PRIMARY KEY (director_id)
);

ALTER TABLE director ADD CONSTRAINT director_country_country_name_fk FOREIGN KEY (country_name) REFERENCES  country(country_name);


CREATE TABLE producer (
	producer_id integer NOT NULL GENERATED ALWAYS AS IDENTITY ,
	gender varchar(6) NOT NULL,
	fname varchar(50) NOT NULL,
	mname varchar(2),
	lname varchar(50) NOT NULL,
	date_of_birth date NOT NULL,
    image varchar(100),
    country_name varchar(100),
	description text,
	instagram varchar(100),
	twitter varchar(100),
	linkedin varchar(100),
    age numeric GENERATED ALWAYS AS (2020 - date_part('year', date_of_birth)) STORED,
	CONSTRAINT producer_pk PRIMARY KEY (producer_id)

);

ALTER TABLE producer ADD CONSTRAINT producer_country_country_name_fk FOREIGN KEY (country_name) REFERENCES  country(country_name);

CREATE FUNCTION compute_age() RETURNS trigger AS $compute_age$
    BEGIN
        NEW.age = date_part('year', now()) - date_part('year', NEW.date_of_birth);
        RETURN NEW;
    END;
$compute_age$ LANGUAGE plpgsql;

CREATE TRIGGER compute_age AFTER INSERT OR UPDATE ON actor
    FOR EACH ROW EXECUTE FUNCTION compute_age();

CREATE TRIGGER compute_age AFTER INSERT OR UPDATE ON director
    FOR EACH ROW EXECUTE FUNCTION compute_age();

CREATE TRIGGER compute_age AFTER INSERT OR UPDATE ON producer
    FOR EACH ROW EXECUTE FUNCTION compute_age();

CREATE TABLE rating (
    rating_id integer NOT NULL GENERATED ALWAYS AS IDENTITY ,
	numeric_rating integer,
	movie_id_movie integer,
	user_id_user integer
);



ALTER TABLE rating ADD CONSTRAINT movie_fk FOREIGN KEY (movie_id_movie)
REFERENCES movie (movie_id) MATCH FULL
ON DELETE CASCADE ON UPDATE CASCADE;

CREATE TABLE many_movie_has_many_genre (
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ,
	movie_id_movie integer NOT NULL,
	name_genre varchar(50) NOT NULL,
	CONSTRAINT many_movie_has_many_genre_pk PRIMARY KEY (id)
);

ALTER TABLE many_movie_has_many_genre ADD CONSTRAINT movie_fk FOREIGN KEY (movie_id_movie)
REFERENCES movie (movie_id) MATCH FULL
ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE many_movie_has_many_genre ADD CONSTRAINT genre_fk FOREIGN KEY (name_genre)
REFERENCES genre (name) MATCH FULL
ON DELETE CASCADE ON UPDATE CASCADE;

CREATE TABLE many_movie_has_many_producer (
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ,
	movie_id_movie integer NOT NULL,
	producer_id_producer integer NOT NULL,
	CONSTRAINT many_movie_has_many_producer_pk PRIMARY KEY (id)
);

ALTER TABLE many_movie_has_many_producer ADD CONSTRAINT movie_fk FOREIGN KEY (movie_id_movie)
REFERENCES movie (movie_id) MATCH FULL
ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE many_movie_has_many_producer ADD CONSTRAINT producer_fk FOREIGN KEY (producer_id_producer)
REFERENCES producer (producer_id) MATCH FULL
ON DELETE CASCADE ON UPDATE CASCADE;

CREATE TABLE many_movie_has_many_director (
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ,
	movie_id_movie integer NOT NULL,
	director_id_director integer NOT NULL,
	CONSTRAINT many_movie_has_many_director_pk PRIMARY KEY (id)
);

ALTER TABLE many_movie_has_many_director ADD CONSTRAINT movie_fk FOREIGN KEY (movie_id_movie)
REFERENCES movie (movie_id) MATCH FULL
ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE many_movie_has_many_director ADD CONSTRAINT director_fk FOREIGN KEY (director_id_director)
REFERENCES director (director_id) MATCH FULL
ON DELETE CASCADE ON UPDATE CASCADE;

CREATE TABLE many_movie_has_many_actor (
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ,
	movie_id_movie integer NOT NULL,
	actor_id_actor integer NOT NULL,
	CONSTRAINT many_movie_has_many_actor_pk PRIMARY KEY (id)

);

ALTER TABLE many_movie_has_many_actor ADD CONSTRAINT movie_fk FOREIGN KEY (movie_id_movie)
REFERENCES movie (movie_id) MATCH FULL
ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE many_movie_has_many_actor ADD CONSTRAINT actor_fk FOREIGN KEY (actor_id_actor)
REFERENCES actor (actor_id) MATCH FULL
ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE rating ADD CONSTRAINT user_fk FOREIGN KEY (user_id_user)
REFERENCES "MovieForumApp_user" (id) MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;

CREATE TABLE favorite
(
    favorite_id      integer GENERATED ALWAYS AS IDENTITY ,
    movie_id_movie integer
        CONSTRAINT movie_fk
            REFERENCES movie
            ON UPDATE CASCADE ON DELETE CASCADE,
    user_id_user   integer
        CONSTRAINT user_fk
            REFERENCES "MovieForumApp_user"
            ON UPDATE CASCADE ON DELETE SET NULL
);





CREATE TABLE comment (
	comment_id integer NOT NULL GENERATED ALWAYS AS IDENTITY ,
	content text,
	creation_date timestamp,
	movie_id_movie integer,
	user_id_user integer,
	CONSTRAINT comment_pk PRIMARY KEY (comment_id)

);

CREATE TABLE reply (
	reply_id integer NOT NULL GENERATED ALWAYS AS IDENTITY ,
	content text,
    creation_date timestamp,
	comment_id_comment integer,
    user_id_user integer,
	CONSTRAINT reply_pk PRIMARY KEY (reply_id)

);

ALTER TABLE comment ADD CONSTRAINT user_fk FOREIGN KEY (user_id_user)
REFERENCES "MovieForumApp_user" (id) MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;

ALTER TABLE comment ADD CONSTRAINT movie_fk FOREIGN KEY (movie_id_movie)
REFERENCES movie (movie_id) MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;

ALTER TABLE reply ADD CONSTRAINT comment_fk FOREIGN KEY (comment_id_comment)
REFERENCES comment (comment_id) MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;

ALTER TABLE reply ADD CONSTRAINT user_fk FOREIGN KEY (user_id_user)
REFERENCES "MovieForumApp_user" (id) MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;




-- NOW INSERT STATEMENTS

-- Insert Users
INSERT INTO "MovieForumApp_user" (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined, photo) VALUES (2, 'pbkdf2_sha256$216000$QKBV9o2LvUGn$HLLNU8uGElx4ULadJOcy7RpCuPRiA9dWb0ktU+a+r4o=', '2020-12-07 03:15:06.463468', false, 'Demo', 'Demo', 'User', 'demouser@demo.com', false, true, '2020-12-07 03:15:06.085812', 'image/20/download.png');
INSERT INTO "MovieForumApp_user" (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined, photo) VALUES (3, 'pbkdf2_sha256$216000$ERBf9SIIjrhZ$FGVaClWB5jHQAIjISPzhM5HHHvar3ExlKtUxlKR/3z8=', '2020-12-07 03:22:00.787965', false, 'ege_tan', 'Ege', 'TAN', 'ege.tan@etu.edu.tr', false, true, '2020-12-07 03:22:00.404898', 'image/20/ege_tan.png');
INSERT INTO "MovieForumApp_user" (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined, photo) VALUES (4, 'pbkdf2_sha256$216000$g6k5tTERikJo$uw/m4RUKHqjNr7iBJzdeSQx95lw4aEfISkOYazD46aI=', '2020-12-07 03:22:22.164286', false, 'alper_kaan_yildiz', 'Alper Kaan', 'YILDIZ', 'a.yildiz@etu.edu.tr', false, true, '2020-12-07 03:22:21.775546', 'image/20/alper_kaan_yildiz.png');
INSERT INTO "MovieForumApp_user" (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined, photo) VALUES (5, 'pbkdf2_sha256$216000$RL61TOwiWpMt$Hz//9+JCGlFL4gGVH/zQ8OlVmbuMv6OJHqNJqSWhMNo=', '2020-12-07 03:22:37.859234', false, 'salih_sert', 'Salih', 'SERT', 's.sert@etu.edu.tr', false, true, '2020-12-07 03:22:37.461098', 'image/20/salih_sert.png');
INSERT INTO "MovieForumApp_user" (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined, photo) VALUES (6, 'pbkdf2_sha256$216000$TTtDPgHAefdr$HRARyMNBqe+0RKKXgdGnjH8Psen34k5EPEg8GN/rQvQ=', '2020-12-07 03:22:58.110711', false, 'tansel_ozyer', 'Tansel', 'ÖZYER', 'ozyer@etu.edu.tr', false, true, '2020-12-07 03:22:57.705367', 'image/20/tansel_ozyer.jpg');

-- Insert Genres
INSERT INTO genre (name) VALUES ('Horror');
INSERT INTO genre (name) VALUES ('Sci-Fi');
INSERT INTO genre (name) VALUES ('Comedy');
INSERT INTO genre (name) VALUES ('Action');
INSERT INTO genre (name) VALUES ('Adventure');
INSERT INTO genre (name) VALUES ('Drama');
INSERT INTO genre (name) VALUES ('Fantasy');
INSERT INTO genre (name) VALUES ('Crime');
INSERT INTO genre (name) VALUES ('Romance');
INSERT INTO genre (name) VALUES ('Political');

-- Insert Countries
INSERT INTO country (country_name) VALUES ('Turkey');
INSERT INTO country (country_name) VALUES ('Germany');
INSERT INTO country (country_name) VALUES ('England');
INSERT INTO country (country_name) VALUES ('Belgium');
INSERT INTO country (country_name) VALUES ('France');
INSERT INTO country (country_name) VALUES ('Spain');
INSERT INTO country (country_name) VALUES ('USA');
INSERT INTO country (country_name) VALUES ('Mexico');
INSERT INTO country (country_name) VALUES ('Russia');
INSERT INTO country (country_name) VALUES ('Bulgaria');


-- Insert Actors
INSERT INTO actor (gender, fname, mname, lname, date_of_birth, image, country_name, description, instagram, twitter, linkedin) VALUES ('Male', 'Bruce', null, 'Willis', '1955-03-25', 'image/20/bruce_willis_z3NKCfS.jpg', 'USA', 'Actor and musician Bruce Willis is well known for playing wisecracking or hard-edged characters, often in spectacular action films. Collectively, he has appeared in films that have grossed in excess of $2.5 billion USD, placing him in the top ten stars in terms of box office receipts.

Walter Bruce Willis was born on March 19, 1955, in Idar-Oberstein, West Germany, to a German mother, Marlene Kassel, and an American father, David Andrew Willis (from Carneys Point, New Jersey), who were then living on a United States military base. His family moved to the U.S. shortly after he was born, and he was raised in Penns Grove, New Jersey, where his mother worked at a bank and his father was a welder and factory worker. Willis picked up an interest for the dramatic arts in high school, and was allegedly "discovered" whilst working in a café in New York City and then appeared in a couple of off-Broadway productions. While bartending one night, he was seen by a casting director who liked his personality and needed a bartender for a small movie role.', 'https://www.instagram.com/brucewillisbw/?hl=en', 'https://twitter.com/bruceywillis?lang=en', 'https://www.linkedin.com/in/bruce-willis-147068a6');
INSERT INTO actor (gender, fname, mname, lname, date_of_birth, image, country_name, description, instagram, twitter, linkedin) VALUES ('Male', 'Morgan', 'J.', 'Freeman', '1937-06-01', 'image/20/morgan_freeman.jpg', 'USA', 'With an authoritative voice and calm demeanor, this ever popular American actor has grown into one of the most respected figures in modern US cinema. Morgan was born on June 1, 1937 in Memphis, Tennessee, to Mayme Edna (Revere), a teacher, and Morgan Porterfield Freeman, a barber. The young Freeman attended Los Angeles City College before serving several years in the US Air Force as a mechanic between 1955 and 1959. His first dramatic arts exposure was on the stage including appearing in an all-African American production of the exuberant musical Hello, Dolly!.

Throughout the 1970s, he continued his work on stage, winning Drama Desk and Clarence Derwent Awards and receiving a Tony Award nomination for his performance in The Mighty Gents in 1978. In 1980, he won two Obie Awards, for his portrayal of Shakespearean anti-hero Coriolanus at the New York Shakespeare Festival and for his work in Mother Courage and Her Children. Freeman won another Obie in 1984 for his performance as The Messenger in the acclaimed Brooklyn Academy of Music production of Lee Breuer''s The Gospel at Colonus and, in 1985, won the Drama-Logue Award for the same role. In 1987, Freeman created the role of Hoke Coleburn in Alfred Uhry''s Pulitzer Prize-winning play Driving Miss Daisy, which brought him his fourth Obie Award. In 1990, Freeman starred as Petruchio in the New York Shakespeare Festival''s The Taming of the Shrew, opposite Tracey Ullman. Returning to the Broadway stage in 2008, Freeman starred with Frances McDormand and Peter Gallagher in Clifford Odets'' drama The Country Girl, directed by Mike Nichols.', 'https://www.instagram.com/morganfreeman/?hl=en', 'https://twitter.com/mjfree', 'https://www.linkedin.com/in/morgan-freeman-4ab95a81');
INSERT INTO actor (gender, fname, mname, lname, date_of_birth, image, country_name, description, instagram, twitter, linkedin) VALUES ('Male', 'Leonardo', null, 'DiCaprio', '1974-11-11', 'image/20/leonardo_dicaprio.jpg', 'USA', 'Few actors in the world have had a career quite as diverse as Leonardo DiCaprio''s. DiCaprio has gone from relatively humble beginnings, as a supporting cast member of the sitcom Growing Pains (1985) and low budget horror movies, such as Critters 3 (1991), to a major teenage heartthrob in the 1990s, as the hunky lead actor in movies such as Romeo + Juliet (1996) and Titanic (1997), to then become a leading man in Hollywood blockbusters, made by internationally renowned directors such as Martin Scorsese and Christopher Nolan.

Leonardo Wilhelm DiCaprio was born November 11, 1974 in Los Angeles, California, the only child of Irmelin DiCaprio (née Indenbirken) and former comic book artist George DiCaprio. His father is of Italian and German descent, and his mother, who is German-born, is of German and Russian ancestry. His middle name, "Wilhelm", was his maternal grandfather''s first name. Leonardo''s father had achieved minor status as an artist and distributor of cult comic book titles, and was even depicted in several issues of American Splendor, the cult semi-autobiographical comic book series by the late ''Harvey Pekar'', a friend of George''s. Leonardo''s performance skills became obvious to his parents early on, and after signing him up with a talent agent who wanted Leonardo to perform under the stage name "Lenny Williams", DiCaprio began appearing on a number of television commercials and educational programs.', 'https://www.instagram.com/leonardodicaprio/?hl=en', 'https://twitter.com/LeoDiCaprio?ref_src=twsrc%5Egoogle%7Ctwcamp%5Eserp%7Ctwgr%5Eauthor', 'https://www.linkedin.com/in/leonardo-dicaprio-847265118');
INSERT INTO actor (gender, fname, mname, lname, date_of_birth, image, country_name, description, instagram, twitter, linkedin) VALUES ('Male', 'Kıvanç', null, 'Tatlıtuğ', '1983-10-27', 'image/20/kivanc_tatlitug.jpg', 'Turkey', 'Kıvanç Tatlıtuğ (Turkish pronunciation: [kɯˈvantʃ ˈtatɫɯtuː]; born 27 October 1983)[2] is a Turkish actor, model, and former basketball player. He is one of the highest-paid actors in Turkey and has won many awards, including three Golden Butterfly Awards and a Yeşilçam Cinema Award. Tatlıtuğ won the pageants Best Model of Turkey and Best Model of the World in 2002.[3][4] Tatlıtuğ has established himself as a leading actor of Turkey with roles in several of the highly successful television series, that includes Menekşe ile Halil (2007–2008), Aşk-ı Memnu (2008–2010), Kuzey Güney (2011–2013) and Cesur ve Güzel (2016–2017), all of which garnered him critical acclaim and international recognition', 'https://www.instagram.com/kivanctatlitug/?hl=en', 'https://twitter.com/kivanctatlitug?lang=en', 'https://tr.linkedin.com/in/kivanc-tatlitug-a83704b7');