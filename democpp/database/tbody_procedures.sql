-- Insert
CREATE OR REPLACE FUNCTION neuron_schema.pInstBody(
	IN	p_name				neuron_schema.tBody.name%TYPE default NULL
	) RETURNS bigint AS $$
DECLARE
	v_id					neuron_schema.tBody.id%TYPE := NULL;
BEGIN
	-- Get ID
	SELECT
		*
	INTO
		v_id
	FROM
		LASTVAL()
	;
	-- Insert
	INSERT INTO
		neuron_schema.tBody
		(
			id,
			name
		)
	VALUES
		(
			v_id,
			p_name
		)
	;

-- Return ID
	RETURN v_id;
END;
$$ LANGUAGE plpgsql
CALLED ON NULL INPUT
;

-- Update
CREATE OR REPLACE FUNCTION neuron_schema.pUpdtBody(
	IN	p_id				neuron_schema.tBody.id%TYPE default NULL,
	IN	p_name				neuron_schema.tBody.name%TYPE default NULL
	) RETURNS bigint AS $$
DECLARE
	v_id					neuron_schema.tBody.id%TYPE := NULL;
	v_name					neuron_schema.tBody.name%TYPE;
BEGIN
	-- Get current Data and lock it
	SELECT
		id,
		COALESCE(p_name, name)
	INTO
		v_id,
		v_name
	FROM
		neuron_schema.tBody
	WHERE
		id = p_id
	FOR UPDATE
	;
	-- Compare values for each entry
	IF v_name != p_name AND p_name IS NOT NULL THEN
		v_name := p_name;
	END IF;
	-- Update data
	UPDATE
		neuron_schema.tBody
	SET
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
CREATE OR REPLACE FUNCTION neuron_schema.pDeltBody(
	IN	p_id				neuron_schema.tBody.id%TYPE default NULL,
	IN	p_name				neuron_schema.tBody.name%TYPE default NULL
	) RETURNS void AS $$
BEGIN
	DELETE FROM
		neuron_schema.tBody
	WHERE
		id = p_id
	AND
		name = p_name
	;
END;
$$ LANGUAGE plpgsql
CALLED ON NULL INPUT
;
