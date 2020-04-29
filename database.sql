
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
-- Table: neuron_schema.tattachment
--

-- SEQUENCE: neuron_schema.tattachment_id_seq

-- DROP SEQUENCE neuron_schema.tattachment_id_seq;

CREATE SEQUENCE neuron_schema.tattachment_id_seq;

ALTER SEQUENCE neuron_schema.tattachment_id_seq
	OWNER TO neuron;


-- DROP TABLE neuron_schema.tattachment;

CREATE TABLE neuron_schema.tattachment
(
	id bigint NOT NULL DEFAULT nextval('neuron_schema.tattachment_id_seq'::regclass),
	attachment text COLLATE pg_catalog."default" NOT NULL,
	CONSTRAINT pk_attachment_id PRIMARY KEY (id)
)
WITH (
	OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE neuron_schema.tattachment
	OWNER to neuron;

-- Index: idx_attachment_id

-- DROP INDEX neuron_schema.idx_attachment_id;

CREATE INDEX idx_attachment_id
	ON neuron_schema.tattachment USING btree
	(id)
	TABLESPACE pg_default;

-- Index: idx_attachment_attachment

-- DROP INDEX neuron_schema.idx_attachment_attachment;

CREATE INDEX idx_attachment_attachment
	ON neuron_schema.tattachment USING btree
	(attachment COLLATE pg_catalog."default")
	TABLESPACE pg_default;

--
-- Table: neuron_schema.tlocation
--

-- SEQUENCE: neuron_schema.tlocation_id_seq

-- DROP SEQUENCE neuron_schema.tlocation_id_seq;

CREATE SEQUENCE neuron_schema.tlocation_id_seq;

ALTER SEQUENCE neuron_schema.tlocation_id_seq
	OWNER TO neuron;


-- DROP TABLE neuron_schema.tlocation;

CREATE TABLE neuron_schema.tlocation
(
	id bigint NOT NULL DEFAULT nextval('neuron_schema.tlocation_id_seq'::regclass),
	location_name text COLLATE pg_catalog."default" NOT NULL,
	attachment_id bigint NOT NULL,
	CONSTRAINT pk_location_id PRIMARY KEY (id),
	CONSTRAINT fk_location_attachment_id FOREIGN KEY (attachment_id)
		REFERENCES neuron_schema.tattachment (id) MATCH SIMPLE
		ON UPDATE NO ACTION
		ON DELETE NO ACTION
)
WITH (
	OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE neuron_schema.tlocation
	OWNER to neuron;


-- Index: idx_location_id

-- DROP INDEX neuron_schema.idx_location_id;

CREATE INDEX idx_location_id
	ON neuron_schema.tlocation USING btree
	(id)
	TABLESPACE pg_default;

-- Index: fk_location_attachment_id

-- DROP INDEX neuron_schema.fk_location_attachment_id;

CREATE INDEX fk_location_attachment_id
	ON neuron_schema.tlocation USING btree
	(attachment_id)
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

----
---- Neurotransmitter Data
----

--
-- Table: neuron_schema.tneurotransmitter
--

-- SEQUENCE: neuron_schema.tneurotransmitter_id_seq

-- DROP SEQUENCE neuron_schema.tneurotransmitter_id_seq;

CREATE SEQUENCE neuron_schema.tneurotransmitter_id_seq;

ALTER SEQUENCE neuron_schema.tneurotransmitter_id_seq
	OWNER TO neuron;

-- DROP TABLE neuron_schema.tneurotransmitter;

CREATE TABLE neuron_schema.tneurotransmitter
(
	id bigint NOT NULL DEFAULT nextval('neuron_schema.tneurotransmitter_id_seq'::regclass),
	name text COLLATE pg_catalog."default" NOT NULL,
	excitatory boolean NOT NULL,
	inhibitory boolean NOT NULL,
	CONSTRAINT tneurotransmitter_pkey PRIMARY KEY (id)
)
WITH (
	OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE neuron_schema.tneurotransmitter
	OWNER to neuron;

-- Index: idx_neurotransmitter_id

-- DROP INDEX neuron_schema.idx_neurotransmitter_id;

CREATE UNIQUE INDEX idx_neurotransmitter_id
	ON neuron_schema.tneurotransmitter USING btree
	(id)
	TABLESPACE pg_default;


--
-- Table: neuron_schema.tcelltype
--

-- SEQUENCE: neuron_schema.tcelltype_id_seq

-- DROP SEQUENCE neuron_schema.tcelltype_id_seq;

CREATE SEQUENCE neuron_schema.tcelltype_id_seq;

ALTER SEQUENCE neuron_schema.tcelltype_id_seq
	OWNER TO neuron;

-- DROP TABLE neuron_schema.tcelltype;

CREATE TABLE neuron_schema.tcelltype
(
	id bigint NOT NULL DEFAULT nextval('neuron_schema.tcelltype_id_seq'::regclass),
	name text COLLATE pg_catalog."default" NOT NULL,
	output_neurotransmitter_id bigint NOT NULL,
	iotype "char" NOT NULL DEFAULT 'S'::bpchar,
	CONSTRAINT tcelltype_pkey PRIMARY KEY (id),
	CONSTRAINT u_celltype_01 UNIQUE (name),
	CONSTRAINT u_celltype_02 UNIQUE (name, output_neurotransmitter_id),
	CONSTRAINT fk_celltype_output_neurotransmitter_id FOREIGN KEY (output_neurotransmitter_id)
		REFERENCES neuron_schema.tneurotransmitter (id) MATCH SIMPLE
		ON UPDATE NO ACTION
		ON DELETE NO ACTION,
	CONSTRAINT ck_tcelltype_iotype CHECK (iotype::text = ANY (ARRAY['M'::bpchar, 'S'::bpchar]::text[]))
)
WITH (
	OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE neuron_schema.tcelltype
	OWNER to neuron;

-- Index: idx_celltype_id

-- DROP INDEX neuron_schema.idx_celltype_id;

CREATE UNIQUE INDEX idx_celltype_id
	ON neuron_schema.tcelltype USING btree
	(id)
	TABLESPACE pg_default;

-- Index: idx_celltype_name

-- DROP INDEX neuron_schema.idx_celltype_name;

CREATE UNIQUE INDEX idx_celltype_name
	ON neuron_schema.tcelltype USING btree
	(name)
	TABLESPACE pg_default;


-- Index: idx_celltype_neurontransmitter_id

-- DROP INDEX neuron_schema.idx_celltype_neurontransmitter_id;

CREATE INDEX idx_celltype_neurontransmitter_id
	ON neuron_schema.tcelltype USING btree
	(output_neurotransmitter_id)
	TABLESPACE pg_default;

-- Index: idx_celltype_iotype

-- DROP INDEX neuron_schema.idx_celltype_iotype;

CREATE INDEX idx_celltype_iotype
	ON neuron_schema.tcelltype USING btree
	(iotype)
	TABLESPACE pg_default;


--
-- Table: neuron_schema.tneurotransmittercelltype
--

-- SEQUENCE: neuron_schema.tneurotransmittercelltype_id_seq

-- DROP SEQUENCE neuron_schema.tneurotransmittercelltype_id_seq;

CREATE SEQUENCE neuron_schema.tneurotransmittercelltype_id_seq;

ALTER SEQUENCE neuron_schema.tneurotransmittercelltype_id_seq
	OWNER TO neuron;


-- DROP TABLE neuron_schema.tneurotransmittercelltype;

CREATE TABLE neuron_schema.tneurotransmittercelltype
(
	id bigint NOT NULL DEFAULT nextval('neuron_schema.tneurotransmittercelltype_id_seq'::regclass),
	celltype_id bigint NOT NULL,
	input_neurotransmitter_id bigint NOT NULL,
	CONSTRAINT pkneurotransmittercelltype_id PRIMARY KEY (id),
	CONSTRAINT u_neurotransmittercelltype_01 UNIQUE (celltype_id, input_neurotransmitter_id),
	CONSTRAINT fk_neurotransmittercelltype_id FOREIGN KEY (celltype_id)
		REFERENCES neuron_schema.tcelltype (id) MATCH SIMPLE
		ON UPDATE NO ACTION
		ON DELETE NO ACTION,
	CONSTRAINT fk_neurotransmittercelltype_input_neurotransmitter_id FOREIGN KEY (input_neurotransmitter_id)
		REFERENCES neuron_schema.tneurotransmitter (id) MATCH SIMPLE
		ON UPDATE NO ACTION
		ON DELETE NO ACTION
)
WITH (
	OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE neuron_schema.tneurotransmittercelltype
	OWNER to neuron;

-- Index: idx_neuroncelltype_id

-- DROP INDEX neuron_schema.idx_neuroncelltype_id;

CREATE INDEX idx_neuroncelltype_id
	ON neuron_schema.tneurotransmittercelltype USING btree
	(id)
	TABLESPACE pg_default;

-- Index: idx_neuroncelltype_celltype_id

-- DROP INDEX neuron_schema.idx_neuroncelltype_celltype_id;

CREATE INDEX idx_neuroncelltype_celltype_id
	ON neuron_schema.tneurotransmittercelltype USING btree
	(celltype_id)
	TABLESPACE pg_default;

-- Index: idx_neuroncelltype_neurotransmitter_id

-- DROP INDEX neuron_schema.idx_neuroncelltype_neurotransmitter_id;

CREATE INDEX idx_neuroncelltype_neurotransmitter_id
	ON neuron_schema.tneurotransmittercelltype USING btree
	(input_neurotransmitter_id)
	TABLESPACE pg_default;




----
---- Body Neuron Descriptions
----

--
-- Table: neuron_schema.tbodymap
--

-- SEQUENCE: neuron_schema.tbodymap_id_seq

-- DROP SEQUENCE neuron_schema.tbodymap_id_seq;

CREATE SEQUENCE neuron_schema.tbodymap_id_seq;

ALTER SEQUENCE neuron_schema.tbodymap_id_seq
	OWNER TO neuron;

-- DROP TABLE neuron_schema.tbodymap;

CREATE TABLE neuron_schema.tbodymap
(
	id bigint NOT NULL DEFAULT nextval('neuron_schema.tbodymap_id_seq'::regclass),
	body_id bigint NOT NULL,
	location_id bigint NOT NULL,
	CONSTRAINT tbodymap_pkey PRIMARY KEY (id),
	CONSTRAINT u_bodymap_01 UNIQUE (body_id, location_id),
	CONSTRAINT fk_bodymap_body_id FOREIGN KEY (body_id)
		REFERENCES neuron_schema.tbody (id) MATCH SIMPLE
		ON UPDATE NO ACTION
		ON DELETE NO ACTION
)
WITH (
	OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE neuron_schema.tbodymap
	OWNER to neuron;


-- Index: idx_bodymap_id

-- DROP INDEX neuron_schema.idx_bodymap_id;

CREATE UNIQUE INDEX idx_bodymap_id
	ON neuron_schema.tbodymap USING btree
	(id)
	TABLESPACE pg_default;


-- Index: fki_bodymap_body_id

-- DROP INDEX neuron_schema.fki_bodymap_body_id;

CREATE INDEX fki_bodymap_body_id
	ON neuron_schema.tbodymap USING btree
	(body_id)
	TABLESPACE pg_default;

-- Index: idx_bodymap_location_id

-- DROP INDEX neuron_schema.idx_bodymap_location_id;

CREATE UNIQUE INDEX idx_bodymap_location_id
	ON neuron_schema.tbodymap USING btree
	(location_id)
	TABLESPACE pg_default;


--
-- Table: neuron_schema.tbodyneuronmap
--

-- SEQUENCE: neuron_schema.tbodyneuronmap_id_seq

-- DROP SEQUENCE neuron_schema.tbodyneuronmap_id_seq;

CREATE SEQUENCE neuron_schema.tbodyneuronmap_id_seq;

ALTER SEQUENCE neuron_schema.tbodyneuronmap_id_seq
	OWNER TO neuron;


-- DROP TABLE neuron_schema.tbodyneuronmap;

CREATE TABLE neuron_schema.tbodyneuronmap
(
	id bigint NOT NULL DEFAULT nextval('neuron_schema.tbodyneuronmap_id_seq'::regclass),
	bodymap_id bigint NOT NULL,
	celltype_id bigint NOT NULL,
	CONSTRAINT pk_bodyneuronmap_id PRIMARY KEY (id),
	CONSTRAINT fk_bodyneuronmap_bodymap_id FOREIGN KEY (bodymap_id)
		REFERENCES neuron_schema.tbodymap (id) MATCH SIMPLE
		ON UPDATE NO ACTION
		ON DELETE NO ACTION,
	CONSTRAINT fk_bodyneuronmap_celltype_id FOREIGN KEY (celltype_id)
		REFERENCES neuron_schema.tcelltype (id) MATCH SIMPLE
		ON UPDATE NO ACTION
		ON DELETE NO ACTION
)
WITH (
	OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE neuron_schema.tbodyneuronmap
	OWNER to neuron;

-- Index: idx_bodyneuronmap_id

-- DROP INDEX neuron_schema.idx_bodyneuronmap_id;

CREATE INDEX idx_bodyneuronmap_id
	ON neuron_schema.tbodyneuronmap USING btree
	(id)
	TABLESPACE pg_default;

-- Index: idx_bodyneuronmap_bodymap_id

-- DROP INDEX neuron_schema.idx_bodyneuronmap_bodymap_id;

CREATE INDEX idx_bodyneuronmap_bodymap_id
	ON neuron_schema.tbodyneuronmap USING btree
	(bodymap_id)
	TABLESPACE pg_default;

-- Index: idx_bodyneuronmap_celltype_id

-- DROP INDEX neuron_schema.idx_bodyneuronmap_celltype_id;

CREATE INDEX idx_bodyneuronmap_celltype_id
	ON neuron_schema.tbodyneuronmap USING btree
	(celltype_id)
	TABLESPACE pg_default;

-- Index: idx_bodyneuronmap_celltype_id

-- DROP INDEX neuron_schema.idx_bodyneuronmap_celltype_id;

CREATE INDEX idx_bodyneuronmap_celltype_id
	ON neuron_schema.tbodyneuronmap USING btree
	(celltype_id)
	TABLESPACE pg_default;

----
---- Individual-Body-Specific Neuron Information
----

--
-- Table: neuron_schema.tneuron
--

-- SEQUENCE: neuron_schema.tneuron_id_seq

-- DROP SEQUENCE neuron_schema.tneuron_id_seq;

CREATE SEQUENCE neuron_schema.tneuron_id_seq;

ALTER SEQUENCE neuron_schema.tneuron_id_seq
	OWNER TO neuron;


-- DROP TABLE neuron_schema.tneuron;

CREATE TABLE neuron_schema.tneuron
(
	id bigint NOT NULL DEFAULT nextval('neuron_schema.tneuron_id_seq'::regclass),
	individual_id bigint NOT NULL,
	bodyneuronmap_id bigint NOT NULL,
	name text COLLATE pg_catalog."default" NOT NULL,
	CONSTRAINT pk_neuron_id PRIMARY KEY (id),
	CONSTRAINT fk_neuron_bodyneuronmap_id FOREIGN KEY (bodyneuronmap_id)
		REFERENCES neuron_schema.tbodyneuronmap (id) MATCH SIMPLE
		ON UPDATE NO ACTION
		ON DELETE NO ACTION,
	CONSTRAINT fk_neuron_individual_id FOREIGN KEY (individual_id)
		REFERENCES neuron_schema.tindividual (id) MATCH SIMPLE
		ON UPDATE NO ACTION
		ON DELETE NO ACTION
)
WITH (
	OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE neuron_schema.tneuron
	OWNER to neuron;

-- Index: idx_neuron_id

-- DROP INDEX neuron_schema.idx_neuron_id;

CREATE UNIQUE INDEX idx_neuron_id
	ON neuron_schema.tneuron USING btree
	(id)
	TABLESPACE pg_default;

-- Index: idx_neuron_bodyneuronmap_id

-- DROP INDEX neuron_schema.idx_neuron_bodyneuronmap_id;

CREATE INDEX idx_neuron_bodyneuronmap_id
	ON neuron_schema.tneuron USING btree
	(bodyneuronmap_id)
	TABLESPACE pg_default;

-- Index: idx_neuron_individual_id

-- DROP INDEX neuron_schema.idx_neuron_individual_id;

CREATE INDEX idx_neuron_individual_id
	ON neuron_schema.tneuron USING btree
	(individual_id)
	TABLESPACE pg_default;


--
-- Table: neuron_schema.tneuroninput
--

-- SEQUENCE: neuron_schema.tneuroninput_id_seq

-- DROP SEQUENCE neuron_schema.tneuroninput_id_seq;

CREATE SEQUENCE neuron_schema.tneuroninput_id_seq;

ALTER SEQUENCE neuron_schema.tneuroninput_id_seq
	OWNER TO neuron;



-- DROP TABLE neuron_schema.tneuroninput;

CREATE TABLE neuron_schema.tneuroninput
(
	id bigint NOT NULL DEFAULT nextval('neuron_schema.tneuroninput_id_seq'::regclass),
	neuron_id bigint NOT NULL,
	input_transmitter_id bigint NOT NULL,
	total_count bigint NOT NULL default 0,
	threshold_level bigint NOT NULL DEFAULT 1024,
	metabolic_level bigint NOT NULL DEFAULT 512,
	current_level bigint NOT NULL DEFAULT 0,
	CONSTRAINT pk_neuroninput_id PRIMARY KEY (id),
	CONSTRAINT u_neuroninput_u1 UNIQUE (neuron_id, input_transmitter_id),
	CONSTRAINT fk_neuroninput_neuron_id FOREIGN KEY (neuron_id)
		REFERENCES neuron_schema.tneuron (id) MATCH SIMPLE
		ON UPDATE NO ACTION
		ON DELETE NO ACTION,
	CONSTRAINT fk_neuroninput_input_transmitter_id FOREIGN KEY (input_transmitter_id)
		REFERENCES neuron_schema.tneurotransmitter (id) MATCH SIMPLE
		ON UPDATE NO ACTION
		ON DELETE NO ACTION
)
WITH (
	OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE neuron_schema.tneuroninput
	OWNER to neuron;

-- Index: idx_neuroninput_id

-- DROP INDEX neuron_schema.idx_neuroninput_id;

CREATE UNIQUE INDEX idx_neuroninput_id
	ON neuron_schema.tneuroninput USING btree
	(id)
	TABLESPACE pg_default;

-- Index: idx_neuroninput_neuron_id

-- DROP INDEX neuron_schema.idx_neuroninput_neuron_id;

CREATE INDEX idx_neuroninput_neuron_id
	ON neuron_schema.tneuroninput USING btree
	(neuron_id)
	TABLESPACE pg_default;

-- Index: idx_neuroninput_input_transmitter_id

-- DROP INDEX neuron_schema.idx_neuroninput_input_transmitter_id;

CREATE INDEX idx_neuroninput_input_transmitter_id
	ON neuron_schema.tneuroninput USING btree
	(input_transmitter_id)
	TABLESPACE pg_default;


--
-- Table: neuron_schema.tneuronlevel
--

-- SEQUENCE: NONE

-- DROP TABLE neuron_schema.tneuronlevel;

CREATE TABLE neuron_schema.tneuronlevel
(
	neuroninput_id bigint NOT NULL,
	input_level bigint NOT NULL,
	input_level_count bigint NOT NULL default 0,
	CONSTRAINT pk_neuronlevel_id PRIMARY KEY (neuroninput_id),
	CONSTRAINT u_neuronlevel_u1 UNIQUE (neuroninput_id, input_level),
	CONSTRAINT fk_neuronlevel_neuroninput_id FOREIGN KEY (neuroninput_id)
		REFERENCES neuron_schema.tneuroninput (id) MATCH SIMPLE
		ON UPDATE NO ACTION
		ON DELETE NO ACTION
)
WITH (
	OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE neuron_schema.tneuronlevel
	OWNER to neuron;

-- Index: idx_neuronlevel_neuroninput_id

-- DROP INDEX neuron_schema.idx_neuronlevel_neuroninput_id;

CREATE UNIQUE INDEX idx_neuronlevel_neuroninput_id
	ON neuron_schema.tneuronlevel USING btree
	(neuroninput_id)
	TABLESPACE pg_default;

-- Index: idx_neuronlevel_input_level

-- DROP INDEX neuron_schema.idx_neuronlevel_input_level;

CREATE INDEX idx_neuronlevel_input_level
	ON neuron_schema.tneuronlevel USING btree
	(input_level)
	TABLESPACE pg_default;

-- Index: idx_neuronlevel_input_level_count

-- DROP INDEX neuron_schema.idx_neuronlevel_input_level_count;

CREATE INDEX idx_neuronlevel_input_level_count
	ON neuron_schema.tneuronlevel USING btree
	(input_level_count)
	TABLESPACE pg_default;



--
-- Table: neuron_schema.tneurontriggered
--

-- SEQUENCE: NONE

-- DROP TABLE neuron_schema.tneurontriggered;

CREATE TABLE neuron_schema.tneurontriggered
(
	neuroninput_id bigint NOT NULL,
	input_level bigint NOT NULL,
	trigger_time timestamp without time zone NOT NULL,
	CONSTRAINT pk_neurontriggered_id PRIMARY KEY (neuroninput_id),
	CONSTRAINT fk_neurontriggered_neuroninput_id FOREIGN KEY (neuroninput_id)
		REFERENCES neuron_schema.tneuroninput (id) MATCH SIMPLE
		ON UPDATE NO ACTION
		ON DELETE NO ACTION
)
WITH (
	OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE neuron_schema.tneurontriggered
	OWNER to neuron;

-- Index: idx_neurontriggered_neuroninput_id

-- DROP INDEX neuron_schema.idx_neurontriggered_neuroninput_id;

CREATE UNIQUE INDEX idx_neurontriggered_neuroninput_id
	ON neuron_schema.tneurontriggered USING btree
	(neuroninput_id)
	TABLESPACE pg_default;

-- Index: idx_neurontriggered_input_level

-- DROP INDEX neuron_schema.idx_neurontriggered_input_level;

CREATE INDEX idx_neurontriggered_input_level
	ON neuron_schema.tneurontriggered USING btree
	(input_level)
	TABLESPACE pg_default;

-- Index: idx_neurontriggered_trigger_time

-- DROP INDEX neuron_schema.idx_neurontriggered_trigger_time;

CREATE INDEX idx_neurontriggered_trigger_time
	ON neuron_schema.tneurontriggered USING btree
	(trigger_time)
	TABLESPACE pg_default;


----
---- Global Neuron Configuration - NONE
----
