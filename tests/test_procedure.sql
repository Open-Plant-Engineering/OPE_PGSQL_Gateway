CREATE OR REPLACE PROCEDURE public.test_procedure(
    msg text
)
LANGUAGE plpgsql
AS $$
BEGIN
    RAISE NOTICE 'Message: %', msg;
END;
$$;