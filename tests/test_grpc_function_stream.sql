CREATE OR REPLACE FUNCTION public.generate_numbers(
    max_value integer
)
RETURNS TABLE(id integer)
AS $$
BEGIN
    RETURN QUERY
    SELECT *
    FROM generate_series(1, max_value);
END;
$$ LANGUAGE plpgsql;