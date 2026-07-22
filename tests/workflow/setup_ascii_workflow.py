import asyncio

from gee.config.settings import Settings
from gee.postgres.pool import PostgresPool
from gee.postgres.database import DatabaseService


async def main():

    settings = Settings()

    pool = PostgresPool()

    await pool.connect(
        host=settings.pg_host,
        port=settings.pg_port,
        database=settings.pg_database,
        user=settings.pg_user,
        password=settings.pg_password,
    )

    db = DatabaseService(pool)

    print("Dropping table...")

    await db.sql.execute(
        """
        DROP TABLE IF EXISTS workflow_ascii;
        """
    )

    print("Creating table...")

    await db.sql.execute(
        """
        CREATE TABLE workflow_ascii (
            id      integer PRIMARY KEY,
            ascii1  integer NOT NULL,
            ascii2  integer NOT NULL,
            ascii3  integer NOT NULL,
            word    text,
            sum     integer
        );
        """
    )

    print("Loading 50,000 rows...")

    await db.sql.execute(
        """
        INSERT INTO workflow_ascii (
            id,
            ascii1,
            ascii2,
            ascii3
        )
        SELECT
            gs,

            floor(random() * 26 + 65)::int,

            floor(random() * 26 + 65)::int,

            floor(random() * 26 + 65)::int

        FROM generate_series(
            1,
            50000
        ) gs;
        """
    )

    print("Creating procedure...")

    await db.sql.execute(
        """
        CREATE OR REPLACE PROCEDURE public.calculate_ascii_metadata()
        LANGUAGE plpgsql
        AS $$
        BEGIN

            UPDATE workflow_ascii
            SET
                word =
                    chr(ascii1) ||
                    chr(ascii2) ||
                    chr(ascii3),

                sum =
                    ascii1 +
                    ascii2 +
                    ascii3;

        END;
        $$;
        """
    )

    print("Creating function populate_ascii_data...")
    
    await db.sql.execute(
        """
        CREATE OR REPLACE FUNCTION public.populate_ascii_data(
            p_rows integer
        )
        RETURNS integer
        AS $$
        BEGIN
    
            INSERT INTO workflow_ascii (
                id,
                ascii1,
                ascii2,
                ascii3
            )
            SELECT
                gs,
    
                floor(random() * 26 + 65)::int,
                floor(random() * 26 + 65)::int,
                floor(random() * 26 + 65)::int
    
            FROM generate_series(
                1,
                p_rows
            ) gs;
    
            RETURN p_rows;
    
        END;
        $$ LANGUAGE plpgsql;
        """
    )
    
    print("Creating function update_ascii_row...")
    
    await db.sql.execute(
        """
        CREATE OR REPLACE FUNCTION public.update_ascii_row(
            p_id integer,
            p_ascii1 integer,
            p_ascii2 integer,
            p_ascii3 integer
        )
        RETURNS boolean
        AS $$
        BEGIN
    
            UPDATE workflow_ascii
            SET
                ascii1 = p_ascii1,
                ascii2 = p_ascii2,
                ascii3 = p_ascii3
            WHERE id = p_id;
    
            RETURN TRUE;
    
        END;
        $$ LANGUAGE plpgsql;
        """
    )



    rows = await db.sql.execute(
        """
        SELECT COUNT(*) AS total_rows
        FROM workflow_ascii;
        """
    )

    print(
        f"Loaded Rows: {rows[0]['total_rows']}"
    )


if __name__ == "__main__":
    asyncio.run(main())