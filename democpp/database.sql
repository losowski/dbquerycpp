
-- psql -h localhost -d neurondb -U neuron -W
--
-- Create the neuron user for the neuronDB
--
CREATE ROLE neuron LOGIN NOSUPERUSER INHERIT CREATEDB CREATEROLE NOREPLICATION PASSWORD 'neuron';
--
-- Create the database
--
CREATE DATABASE neurondb OWNER neuron;
--
-- Grant privileges
--
GRANT ALL PRIVILEGES ON neurondb TO neuron;

-- SCRIPT BEGIN: set up connection and schema
\connect neurondb
--
-- Create the schema
--
CREATE SCHEMA IF NOT EXISTS neuron_schema AUTHORIZATION neuron;

set schema 'neuron_schema';
-- SCRIPT END
----
---- Body Descriptions
----


--
-- Table: neuron_schema.tbody
--

-- SEQUENCE: neuron_schema.tbody_id_seq

-- DROP SEQUENCE neuron_schema.tbody_id_seq;

CREATE SEQUENCE neuron_schema.tbody_id_seq;

ALTER SEQUENCE neuron_schema.tbody_id_seq
	OWNER TO neuron;


-- DROP TABLE neuron_schema.tbody;

CREATE TABLE neuron_schema.tbody
(
	id bigint NOT NULL DEFAULT nextval('neuron_schema.tbody_id_seq'::regclass),
	name text COLLATE pg_catalog."default" NOT NULL,
	CONSTRAINT pk_tbody PRIMARY KEY (id),
	CONSTRAINT u_body_id UNIQUE (id)

)
WITH (
	OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE neuron_schema.tbody
	OWNER to neuron;

-- Index: idx_body_id

-- DROP INDEX neuron_schema.idx_body_id;

CREATE INDEX idx_body_id
	ON neuron_schema.tbody USING btree
	(id)
	TABLESPACE pg_default;

-- Index: pk_body_name

-- DROP INDEX neuron_schema.pk_body_name;

CREATE UNIQUE INDEX pk_body_name
	ON neuron_schema.tbody USING btree
	(name COLLATE pg_catalog."default")
	TABLESPACE pg_default;

--
-- Table: neuron_schema.tindividual
--

-- SEQUENCE: neuron_schema.tindividual_id_seq

-- DROP SEQUENCE neuron_schema.tindividual_id_seq;

CREATE SEQUENCE neuron_schema.tindividual_id_seq;

ALTER SEQUENCE neuron_schema.tindividual_id_seq
	OWNER TO neuron;


--
-- Table: neuron_schema.tindividual

-- DROP TABLE neuron_schema.tindividual;

CREATE TABLE neuron_schema.tindividual
(
	id bigint NOT NULL DEFAULT nextval('neuron_schema.tindividual_id_seq'::regclass),
	body_id bigint NOT NULL,
	name text COLLATE pg_catalog."default" NOT NULL,
	CONSTRAINT pk_individual_id PRIMARY KEY (id),
	CONSTRAINT u_individual_name UNIQUE (name),
	CONSTRAINT fk_individual_body_id FOREIGN KEY (body_id)
		REFERENCES neuron_schema.tbody (id) MATCH SIMPLE
		ON UPDATE NO ACTION
		ON DELETE NO ACTION
)
WITH (
	OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE neuron_schema.tindividual
	OWNER to neuron;

-- Index: idx_individual_id

-- DROP INDEX neuron_schema.idx_individual_id;

CREATE INDEX idx_individual_id
	ON neuron_schema.tindividual USING btree
	(id)
	TABLESPACE pg_default;

-- Index: pk_individual_name

-- DROP INDEX neuron_schema.pk_individual_name;

CREATE INDEX pk_individual_name
	ON neuron_schema.tindividual USING btree
	(name COLLATE pg_catalog."default")
	TABLESPACE pg_default;

-- Index: idx_individual_body_id

-- DROP INDEX neuron_schema.idx_individual_body_id;

CREATE INDEX idx_individual_body_id
	ON neuron_schema.tindividual USING btree
	(body_id)
	TABLESPACE pg_default;
