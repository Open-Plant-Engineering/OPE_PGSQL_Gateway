CREATE OR REPLACE FUNCTION public.get_numbers()
RETURNS TABLE(
    id integer,
    value text
)
AS $$
BEGIN
    RETURN QUERY
    SELECT 1, 'One'
    UNION ALL
    SELECT 2, 'Two'
    UNION ALL
    SELECT 3, 'Three';
END;
$$ LANGUAGE plpgsql;