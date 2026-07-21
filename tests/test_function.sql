CREATE OR REPLACE FUNCTION public.add_numbers(
    a integer,
    b integer
)
RETURNS integer
AS $$
BEGIN
    RETURN a + b;
END;
$$ LANGUAGE plpgsql;