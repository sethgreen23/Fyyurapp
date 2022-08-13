--
-- PostgreSQL database dump
--

-- Dumped from database version 14.4
-- Dumped by pg_dump version 14.4

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO postgres;

--
-- Name: artist; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.artist (
    id integer NOT NULL,
    name character varying,
    city character varying(120),
    state character varying(120),
    phone character varying(120),
    genres character varying[],
    image_link character varying(500),
    facebook_link character varying(120),
    website character varying(120),
    seeking_venue boolean,
    seeking_description character varying(500)
);


ALTER TABLE public.artist OWNER TO postgres;

--
-- Name: artist_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.artist_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.artist_id_seq OWNER TO postgres;

--
-- Name: artist_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.artist_id_seq OWNED BY public.artist.id;


--
-- Name: show; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.show (
    id integer NOT NULL,
    artist_id integer NOT NULL,
    venue_id integer NOT NULL,
    start_time timestamp without time zone NOT NULL
);


ALTER TABLE public.show OWNER TO postgres;

--
-- Name: show_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.show_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.show_id_seq OWNER TO postgres;

--
-- Name: show_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.show_id_seq OWNED BY public.show.id;


--
-- Name: venue; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.venue (
    id integer NOT NULL,
    name character varying,
    city character varying(120),
    state character varying(120),
    address character varying(120),
    phone character varying(120),
    image_link character varying(500),
    facebook_link character varying(120),
    genres character varying[],
    seeking_description character varying(500),
    seeking_talent boolean,
    website character varying(120)
);


ALTER TABLE public.venue OWNER TO postgres;

--
-- Name: venue_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.venue_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.venue_id_seq OWNER TO postgres;

--
-- Name: venue_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.venue_id_seq OWNED BY public.venue.id;


--
-- Name: artist id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.artist ALTER COLUMN id SET DEFAULT nextval('public.artist_id_seq'::regclass);


--
-- Name: show id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.show ALTER COLUMN id SET DEFAULT nextval('public.show_id_seq'::regclass);


--
-- Name: venue id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.venue ALTER COLUMN id SET DEFAULT nextval('public.venue_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.alembic_version (version_num) FROM stdin;
63ea38ed3c3c
\.


--
-- Data for Name: artist; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.artist (id, name, city, state, phone, genres, image_link, facebook_link, website, seeking_venue, seeking_description) FROM stdin;
2	Guns N Petals	San Francisco	CA	326-123-5000	{"Rock n Roll"}	https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80	https://www.facebook.com/GunsNPetals	https://www.gunsnpetalsband.com	t	Looking for shows to perform at in the San Francisco Bay Area!
3	Matt Quevedo	New York	NY	300-400-5000	{Jazz}	https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80	https://www.facebook.com/mattquevedo923251523		f	
5	Daft Punk	New York	NY	123-541-6524	{Electronic}	https://focus.courrierinternational.com/2022/02/04/0/0/3500/2333/1280/0/60/0/83f70ba_1644013780655-musicdaftpunk.jpg	https://daftpunk.lnk.to/followF	https://www.daftpunk.com/	t	We are looking for a lovely space to perform in
10	Bruno Mars	Los Angeles	CA	123-456-7894	{Classical}	https://www.brunomars.com/sites/g/files/g2000013556/files/2022-01/Artwork_SilkSonic%20%281%29.jpg	https://www.facebook.com/brunomars/	https://www.brunomars.com/	f	
4	The Wild Sax Band	San Francisco	CA	432-325-5432	{Classical,Jazz}	https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80	https://www.facebook.com/bandmix	https://www.bandmix.com/wildsaxshow/	f	
\.


--
-- Data for Name: show; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.show (id, artist_id, venue_id, start_time) FROM stdin;
2	4	4	2022-08-10 17:38:35
3	4	3	2022-08-20 17:38:35
4	4	2	2022-08-29 17:38:35
5	2	3	2022-08-10 17:38:35
6	3	2	2022-08-25 17:38:35
\.


--
-- Data for Name: venue; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.venue (id, name, city, state, address, phone, image_link, facebook_link, genres, seeking_description, seeking_talent, website) FROM stdin;
3	The Dueling Pianos Bar	New York	NY	335 Delancey Street	914-003-1132	https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80	https://www.facebook.com/theduelingpianos	{Classical,Hip-Hop,R&B}		f	https://www.theduelingpianos.com
4	Park Square Live Music & Coffee	San Francisco	CA	34 Whiskey Moore Ave	415-000-1234	https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80	https://www.facebook.com/ParkSquareLiveMusicAndCoffee	{Classical,Folk,Jazz}		f	https://www.parksquarelivemusicandcoffee.com
2	The Musical Hop	San Francisco	CA	1015 Folsom Street	123-123-1234	https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60	https://www.facebook.com/TheMusicalHop	{Classical,Folk,Jazz,Reggae,Soul}	We are on the lookout for a local artist to play every two weeks. Please call us.	t	https://www.themusicalhop.com
5	Love More Event Space	Los Angeles	CA	616  Flower Street 	132-879-8956	https://meetstheeyestudios.com/wp-content/uploads/2015/08/rental-space-party-events-san-carlos.jpg		{Alternative,Electronic,Pop}	Seeking a wonderfull pop groupe to perform	t	https://www.lovemoreevent.com/homepage/
6	Jacob K. Javits Convention Center	New York	NY	655 W 34th St New York NY 10001	212-216-2000	https://scontent.ftun5-1.fna.fbcdn.net/v/t1.18169-9/1922384_10152466783685561_9000197385759928251_n.jpg?_nc_cat=103&ccb=1-7&_nc_sid=d57657&_nc_ohc=vd-s_shgaBgAX9VtvGG&_nc_ht=scontent.ftun5-1.fna&oh=00_AT9Pb3QV1n-OC3Pcr-dI7RT6SwEJeqVbrl8y1usz_0oM0Q&oe=631EDCA5	https://www.facebook.com/profile.php?id=113974405299715	{Blues}		f	https://javitscenter.com/
\.


--
-- Name: artist_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.artist_id_seq', 10, true);


--
-- Name: show_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.show_id_seq', 6, true);


--
-- Name: venue_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.venue_id_seq', 6, true);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: artist artist_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.artist
    ADD CONSTRAINT artist_pkey PRIMARY KEY (id);


--
-- Name: show show_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.show
    ADD CONSTRAINT show_pkey PRIMARY KEY (id);


--
-- Name: venue venue_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.venue
    ADD CONSTRAINT venue_pkey PRIMARY KEY (id);


--
-- Name: show show_artist_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.show
    ADD CONSTRAINT show_artist_id_fkey FOREIGN KEY (artist_id) REFERENCES public.artist(id);


--
-- Name: show show_venue_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.show
    ADD CONSTRAINT show_venue_id_fkey FOREIGN KEY (venue_id) REFERENCES public.venue(id);


--
-- PostgreSQL database dump complete
--

