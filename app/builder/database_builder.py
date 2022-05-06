from databases import Database


async def build_database() -> Database:
    database = Database('postgresql+asyncpg://postgres:pass@api-database:5432/sample-database?ssl=false')
    await database.connect()

    return database
