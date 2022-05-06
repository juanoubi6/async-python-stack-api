from databases import Database

from app.config import DbConfig


async def build_database(db_config: DbConfig) -> Database:
    database = Database(db_config.uri)
    await database.connect()

    return database
