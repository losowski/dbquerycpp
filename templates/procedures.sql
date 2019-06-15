-- Insert
CREATE OR REPLACE FUNCTION neuron_schema.pIns$SQL_TABLENAME(
$SQL_INPUT_PARAMETERS
	) RETURNS bigint AS $$$$
DECLARE
$SQL_DECLARED_PK
BEGIN
	-- Get ID
	SELECT
		*
	INTO
		v_$SQL_PRIMARY_KEY
	FROM
		LASTVAL()
	;
	-- Insert
	INSERT INTO
		$SQL_SCHEMANAME.$SQL_TABLENAME
		(
			$SQL_PRIMARY_KEY,
			$SQL_COLUMNS
		)
	VALUES
		(
			v_$SQL_PRIMARY_KEY
			$SQL_VALUES
		)
	;

-- Return ID
	RETURN v_$SQL_PRIMARY_KEY;
END;
$$$$ LANGUAGE plpgsql
CALLED ON NULL INPUT
;