-- Insert
CREATE OR REPLACE FUNCTION neuron_schema.pInstIndividual(
	IN	p_id				neuron_schema.tIndividual.id%TYPE default NULL,
	IN	p_body_id			neuron_schema.tIndividual.body_id%TYPE default NULL,
	IN	p_name				neuron_schema.tIndividual.name%TYPE default NULL
	) RETURNS bigint AS $$
DECLARE
	v_id					neuron_schema.tIndividual.id%TYPE := NULL;
BEGIN
	INSERT INTO
		neuron_schema.tIndividual
		(
			id,
			body_id,
			name
		)
	VALUES
		(
			p_id,
			p_body_id,
			p_name
		)
	;
	-- Return ID
	SELECT
		*
	INTO
		v_id
	FROM
		LASTVAL()
	;
-- Return ID
	RETURN v_id;
END;
$$ LANGUAGE plpgsql
CALLED ON NULL INPUT
;

-- Update
CREATE OR REPLACE FUNCTION neuron_schema.pUpdtIndividual(
	IN	p_id				neuron_schema.tIndividual.id%TYPE default NULL,
	IN	p_body_id			neuron_schema.tIndividual.body_id%TYPE default NULL,
	IN	p_name				neuron_schema.tIndividual.name%TYPE default NULL
	) RETURNS bigint AS $$
DECLARE
	v_id					neuron_schema.tIndividual.id%TYPE := NULL;
	v_body_id				neuron_schema.tIndividual.body_id%TYPE;
	v_name					neuron_schema.tIndividual.name%TYPE;
BEGIN
	-- Get current Data and lock it
	SELECT
		id,
		COALESCE(p_body_id, body_id),
		COALESCE(p_name, name)
	INTO
		v_id,
		v_body_id
		v_name
	FROM
		neuron_schema.tIndividual
	WHERE
		id = p_id
	FOR UPDATE
	;
	-- Compare values for each entry
	IF v_body_id != p_body_id AND p_body_id IS NOT NULL THEN
		v_body_id := p_body_id;
	END IF;
	IF v_name != p_name AND p_name IS NOT NULL THEN
		v_name := p_name;
	END IF;
	-- Update data
	UPDATE
		neuron_schema.tIndividual
	SET
			body_id = v_body_id,
			name = v_name
	WHERE
		id = v_id
	;
	-- Return ID
	RETURN v_id;
END;
$$ LANGUAGE plpgsql
CALLED ON NULL INPUT
;


-- Delete
CREATE OR REPLACE FUNCTION neuron_schema.pDeltIndividual(
	IN	p_id				neuron_schema.tIndividual.id%TYPE default NULL,
	IN	p_body_id			neuron_schema.tIndividual.body_id%TYPE default NULL,
	IN	p_name				neuron_schema.tIndividual.name%TYPE default NULL
	) RETURNS void AS $$
BEGIN
	DELETE FROM
		neuron_schema.tIndividual
	WHERE
		id = p_id
	AND
		body_id = p_body_id
	AND
		name = p_name
	;
END;
$$ LANGUAGE plpgsql
CALLED ON NULL INPUT
;
