from sqlalchemy import URL, text
from sqlalchemy.engine import make_url
from sqlalchemy.ext.asyncio import create_async_engine


POSTGRES_DEFAULT_DB = "postgres"


async def create_database(url: str | URL):
    url_object = make_url(url)
    database_name = url_object.database
    dbms_url = url_object.set(database=POSTGRES_DEFAULT_DB)
    engine = create_async_engine(dbms_url, isolation_level="AUTOCOMMIT")

    async with engine.connect() as conn:
        c = await conn.execute(
            text(f"SELECT 1 FROM pg_database WHERE datname='{database_name}'")
        )
        database_exists = c.scalar() == 1

    if database_exists:
        await drop_database(url_object)

    async with engine.connect() as conn:
        await conn.execute(
            text(f'CREATE DATABASE "{database_name}" ENCODING "utf8" TEMPLATE template1')
        )
    await engine.dispose()


async def drop_database(url: str | URL):
    url_object = make_url(url)
    db_name = url_object.database
    dbms_url = url_object.set(database=POSTGRES_DEFAULT_DB)
    engine = create_async_engine(dbms_url, isolation_level="AUTOCOMMIT")

    try:
        async with engine.connect() as conn:
            disc_users = """
            SELECT pg_terminate_backend(pid)
            FROM pg_stat_activity
            WHERE pg_stat_activity.datname = :dbname
              AND pid <> pg_backend_pid();
            """
            await conn.execute(text(disc_users), {"dbname": db_name})

            await conn.execute(text(f"DROP DATABASE {db_name}"))
    finally:
        await engine.dispose()
