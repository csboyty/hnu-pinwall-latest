--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: artifact_assets; Type: TABLE; Schema: public; Owner: dbuser; Tablespace: 
--

CREATE TABLE artifact_assets (
    artifact_id integer NOT NULL,
    pos smallint DEFAULT 1 NOT NULL,
    name character varying(256),
    filename character varying(128),
    description text,
    type smallint NOT NULL,
    profile_image character varying(256) NOT NULL,
    media_file character varying(256),
    profile_filename character varying(128) NOT NULL,
    view_url character varying(256)
);


ALTER TABLE public.artifact_assets OWNER TO dbuser;

--
-- Name: artifact_comments; Type: TABLE; Schema: public; Owner: dbuser; Tablespace: 
--

CREATE TABLE artifact_comments (
    id integer NOT NULL,
    artifact_id integer,
    commenter_id integer,
    content text NOT NULL,
    commented_at timestamp without time zone,
    visible boolean
);


ALTER TABLE public.artifact_comments OWNER TO dbuser;

--
-- Name: artifact_comments_id_seq; Type: SEQUENCE; Schema: public; Owner: dbuser
--

CREATE SEQUENCE artifact_comments_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.artifact_comments_id_seq OWNER TO dbuser;

--
-- Name: artifact_comments_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dbuser
--

ALTER SEQUENCE artifact_comments_id_seq OWNED BY artifact_comments.id;


--
-- Name: artifact_scores; Type: TABLE; Schema: public; Owner: dbuser; Tablespace: 
--

CREATE TABLE artifact_scores (
    artifact_id integer NOT NULL,
    scorer_id integer NOT NULL,
    score smallint,
    scored_at timestamp without time zone
);


ALTER TABLE public.artifact_scores OWNER TO dbuser;

--
-- Name: artifact_term; Type: TABLE; Schema: public; Owner: dbuser; Tablespace: 
--

CREATE TABLE artifact_term (
    artifact_id integer NOT NULL,
    term_id integer NOT NULL
);


ALTER TABLE public.artifact_term OWNER TO dbuser;

--
-- Name: artifacts; Type: TABLE; Schema: public; Owner: dbuser; Tablespace: 
--

CREATE TABLE artifacts (
    id integer NOT NULL,
    user_id integer,
    name character varying(256) NOT NULL,
    description text,
    profile_image character varying(256) NOT NULL,
    visible boolean NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone
);


ALTER TABLE public.artifacts OWNER TO dbuser;

--
-- Name: artifacts_id_seq; Type: SEQUENCE; Schema: public; Owner: dbuser
--

CREATE SEQUENCE artifacts_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.artifacts_id_seq OWNER TO dbuser;

--
-- Name: artifacts_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dbuser
--

ALTER SEQUENCE artifacts_id_seq OWNED BY artifacts.id;


--
-- Name: boxview_files; Type: TABLE; Schema: public; Owner: dbuser; Tablespace: 
--

CREATE TABLE boxview_files (
    document_id character varying(32) NOT NULL,
    artifact_id integer NOT NULL,
    media_file character varying NOT NULL,
    result character varying(20),
    created_at timestamp without time zone NOT NULL,
    triggered_at timestamp without time zone
);


ALTER TABLE public.boxview_files OWNER TO dbuser;

--
-- Name: roles; Type: TABLE; Schema: public; Owner: dbuser; Tablespace: 
--

CREATE TABLE roles (
    id integer NOT NULL,
    name character varying(80),
    description character varying(255)
);


ALTER TABLE public.roles OWNER TO dbuser;

--
-- Name: roles_id_seq; Type: SEQUENCE; Schema: public; Owner: dbuser
--

CREATE SEQUENCE roles_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.roles_id_seq OWNER TO dbuser;

--
-- Name: roles_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dbuser
--

ALTER SEQUENCE roles_id_seq OWNED BY roles.id;


--
-- Name: terms; Type: TABLE; Schema: public; Owner: dbuser; Tablespace: 
--

CREATE TABLE terms (
    id integer NOT NULL,
    name character varying(128) NOT NULL
);


ALTER TABLE public.terms OWNER TO dbuser;

--
-- Name: terms_id_seq; Type: SEQUENCE; Schema: public; Owner: dbuser
--

CREATE SEQUENCE terms_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.terms_id_seq OWNER TO dbuser;

--
-- Name: terms_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dbuser
--

ALTER SEQUENCE terms_id_seq OWNED BY terms.id;


--
-- Name: topic_artifact; Type: TABLE; Schema: public; Owner: dbuser; Tablespace: 
--

CREATE TABLE topic_artifact (
    topic_id integer NOT NULL,
    artifact_id integer NOT NULL
);


ALTER TABLE public.topic_artifact OWNER TO dbuser;

--
-- Name: topic_term; Type: TABLE; Schema: public; Owner: dbuser; Tablespace: 
--

CREATE TABLE topic_term (
    topic_id integer NOT NULL,
    term_id integer NOT NULL
);


ALTER TABLE public.topic_term OWNER TO dbuser;

--
-- Name: topics; Type: TABLE; Schema: public; Owner: dbuser; Tablespace: 
--

CREATE TABLE topics (
    id integer NOT NULL,
    user_id integer,
    name character varying(64) NOT NULL,
    description text,
    status smallint,
    created_at timestamp without time zone NOT NULL
);


ALTER TABLE public.topics OWNER TO dbuser;

--
-- Name: topics_id_seq; Type: SEQUENCE; Schema: public; Owner: dbuser
--

CREATE SEQUENCE topics_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.topics_id_seq OWNER TO dbuser;

--
-- Name: topics_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dbuser
--

ALTER SEQUENCE topics_id_seq OWNED BY topics.id;


--
-- Name: user_role; Type: TABLE; Schema: public; Owner: dbuser; Tablespace: 
--

CREATE TABLE user_role (
    user_id integer NOT NULL,
    role_id integer NOT NULL
);


ALTER TABLE public.user_role OWNER TO dbuser;

--
-- Name: user_settings; Type: TABLE; Schema: public; Owner: dbuser; Tablespace: 
--

CREATE TABLE user_settings (
    user_id integer NOT NULL,
    profile_image character varying(256),
    description character varying(1024),
    lang character varying(5) NOT NULL,
    tz character varying(20) NOT NULL,
    comment_active boolean NOT NULL
);


ALTER TABLE public.user_settings OWNER TO dbuser;

--
-- Name: user_tracks; Type: TABLE; Schema: public; Owner: dbuser; Tablespace: 
--

CREATE TABLE user_tracks (
    user_id integer NOT NULL,
    last_login_at timestamp without time zone,
    current_login_at timestamp without time zone,
    last_login_ip character varying(100),
    current_login_ip character varying(100),
    login_count integer
);


ALTER TABLE public.user_tracks OWNER TO dbuser;

--
-- Name: users; Type: TABLE; Schema: public; Owner: dbuser; Tablespace: 
--

CREATE TABLE users (
    id integer NOT NULL,
    email character varying(64),
    fullname character varying(32),
    password character varying(128),
    active boolean,
    confirmed_at timestamp without time zone,
    registered_at timestamp without time zone NOT NULL
);


ALTER TABLE public.users OWNER TO dbuser;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: dbuser
--

CREATE SEQUENCE users_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_id_seq OWNER TO dbuser;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dbuser
--

ALTER SEQUENCE users_id_seq OWNED BY users.id;


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY artifact_comments ALTER COLUMN id SET DEFAULT nextval('artifact_comments_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY artifacts ALTER COLUMN id SET DEFAULT nextval('artifacts_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY roles ALTER COLUMN id SET DEFAULT nextval('roles_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY terms ALTER COLUMN id SET DEFAULT nextval('terms_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY topics ALTER COLUMN id SET DEFAULT nextval('topics_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY users ALTER COLUMN id SET DEFAULT nextval('users_id_seq'::regclass);


--
-- Name: artifact_assets_pkey; Type: CONSTRAINT; Schema: public; Owner: dbuser; Tablespace: 
--

ALTER TABLE ONLY artifact_assets
    ADD CONSTRAINT artifact_assets_pkey PRIMARY KEY (artifact_id, pos);


--
-- Name: artifact_comments_pkey; Type: CONSTRAINT; Schema: public; Owner: dbuser; Tablespace: 
--

ALTER TABLE ONLY artifact_comments
    ADD CONSTRAINT artifact_comments_pkey PRIMARY KEY (id);


--
-- Name: artifact_scores_pkey; Type: CONSTRAINT; Schema: public; Owner: dbuser; Tablespace: 
--

ALTER TABLE ONLY artifact_scores
    ADD CONSTRAINT artifact_scores_pkey PRIMARY KEY (artifact_id, scorer_id);


--
-- Name: artifact_term_pkey; Type: CONSTRAINT; Schema: public; Owner: dbuser; Tablespace: 
--

ALTER TABLE ONLY artifact_term
    ADD CONSTRAINT artifact_term_pkey PRIMARY KEY (artifact_id, term_id);


--
-- Name: artifacts_pkey; Type: CONSTRAINT; Schema: public; Owner: dbuser; Tablespace: 
--

ALTER TABLE ONLY artifacts
    ADD CONSTRAINT artifacts_pkey PRIMARY KEY (id);


--
-- Name: boxview_files_pkey; Type: CONSTRAINT; Schema: public; Owner: dbuser; Tablespace: 
--

ALTER TABLE ONLY boxview_files
    ADD CONSTRAINT boxview_files_pkey PRIMARY KEY (document_id);


--
-- Name: roles_name_key; Type: CONSTRAINT; Schema: public; Owner: dbuser; Tablespace: 
--

ALTER TABLE ONLY roles
    ADD CONSTRAINT roles_name_key UNIQUE (name);


--
-- Name: roles_pkey; Type: CONSTRAINT; Schema: public; Owner: dbuser; Tablespace: 
--

ALTER TABLE ONLY roles
    ADD CONSTRAINT roles_pkey PRIMARY KEY (id);


--
-- Name: terms_name_key; Type: CONSTRAINT; Schema: public; Owner: dbuser; Tablespace: 
--

ALTER TABLE ONLY terms
    ADD CONSTRAINT terms_name_key UNIQUE (name);


--
-- Name: terms_pkey; Type: CONSTRAINT; Schema: public; Owner: dbuser; Tablespace: 
--

ALTER TABLE ONLY terms
    ADD CONSTRAINT terms_pkey PRIMARY KEY (id);


--
-- Name: topic_artifact_pkey; Type: CONSTRAINT; Schema: public; Owner: dbuser; Tablespace: 
--

ALTER TABLE ONLY topic_artifact
    ADD CONSTRAINT topic_artifact_pkey PRIMARY KEY (topic_id, artifact_id);


--
-- Name: topic_term_pkey; Type: CONSTRAINT; Schema: public; Owner: dbuser; Tablespace: 
--

ALTER TABLE ONLY topic_term
    ADD CONSTRAINT topic_term_pkey PRIMARY KEY (topic_id, term_id);


--
-- Name: topics_pkey; Type: CONSTRAINT; Schema: public; Owner: dbuser; Tablespace: 
--

ALTER TABLE ONLY topics
    ADD CONSTRAINT topics_pkey PRIMARY KEY (id);


--
-- Name: user_role_pkey; Type: CONSTRAINT; Schema: public; Owner: dbuser; Tablespace: 
--

ALTER TABLE ONLY user_role
    ADD CONSTRAINT user_role_pkey PRIMARY KEY (user_id, role_id);


--
-- Name: user_settings_pkey; Type: CONSTRAINT; Schema: public; Owner: dbuser; Tablespace: 
--

ALTER TABLE ONLY user_settings
    ADD CONSTRAINT user_settings_pkey PRIMARY KEY (user_id);


--
-- Name: user_tracks_pkey; Type: CONSTRAINT; Schema: public; Owner: dbuser; Tablespace: 
--

ALTER TABLE ONLY user_tracks
    ADD CONSTRAINT user_tracks_pkey PRIMARY KEY (user_id);


--
-- Name: users_email_key; Type: CONSTRAINT; Schema: public; Owner: dbuser; Tablespace: 
--

ALTER TABLE ONLY users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users_pkey; Type: CONSTRAINT; Schema: public; Owner: dbuser; Tablespace: 
--

ALTER TABLE ONLY users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: artifact_assets_artifact_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY artifact_assets
    ADD CONSTRAINT artifact_assets_artifact_id_fkey FOREIGN KEY (artifact_id) REFERENCES artifacts(id) ON DELETE CASCADE;


--
-- Name: artifact_comments_artifact_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY artifact_comments
    ADD CONSTRAINT artifact_comments_artifact_id_fkey FOREIGN KEY (artifact_id) REFERENCES artifacts(id) ON DELETE CASCADE;


--
-- Name: artifact_comments_commenter_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY artifact_comments
    ADD CONSTRAINT artifact_comments_commenter_id_fkey FOREIGN KEY (commenter_id) REFERENCES users(id) ON DELETE CASCADE;


--
-- Name: artifact_scores_artifact_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY artifact_scores
    ADD CONSTRAINT artifact_scores_artifact_id_fkey FOREIGN KEY (artifact_id) REFERENCES artifacts(id) ON DELETE CASCADE;


--
-- Name: artifact_scores_scorer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY artifact_scores
    ADD CONSTRAINT artifact_scores_scorer_id_fkey FOREIGN KEY (scorer_id) REFERENCES users(id) ON DELETE CASCADE;


--
-- Name: artifact_term_artifact_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY artifact_term
    ADD CONSTRAINT artifact_term_artifact_id_fkey FOREIGN KEY (artifact_id) REFERENCES artifacts(id) ON DELETE CASCADE;


--
-- Name: artifact_term_term_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY artifact_term
    ADD CONSTRAINT artifact_term_term_id_fkey FOREIGN KEY (term_id) REFERENCES terms(id) ON DELETE CASCADE;


--
-- Name: artifacts_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY artifacts
    ADD CONSTRAINT artifacts_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;


--
-- Name: topic_artifact_artifact_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY topic_artifact
    ADD CONSTRAINT topic_artifact_artifact_id_fkey FOREIGN KEY (artifact_id) REFERENCES artifacts(id) ON DELETE CASCADE;


--
-- Name: topic_artifact_topic_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY topic_artifact
    ADD CONSTRAINT topic_artifact_topic_id_fkey FOREIGN KEY (topic_id) REFERENCES topics(id) ON DELETE CASCADE;


--
-- Name: topic_term_term_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY topic_term
    ADD CONSTRAINT topic_term_term_id_fkey FOREIGN KEY (term_id) REFERENCES terms(id) ON DELETE CASCADE;


--
-- Name: topic_term_topic_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY topic_term
    ADD CONSTRAINT topic_term_topic_id_fkey FOREIGN KEY (topic_id) REFERENCES topics(id) ON DELETE CASCADE;


--
-- Name: topics_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY topics
    ADD CONSTRAINT topics_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;


--
-- Name: user_role_role_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY user_role
    ADD CONSTRAINT user_role_role_id_fkey FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE;


--
-- Name: user_role_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY user_role
    ADD CONSTRAINT user_role_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;


--
-- Name: user_settings_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY user_settings
    ADD CONSTRAINT user_settings_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;


--
-- Name: user_tracks_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY user_tracks
    ADD CONSTRAINT user_tracks_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO dbuser;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

