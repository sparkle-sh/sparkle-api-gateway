import asyncpg
import asyncio
import os
from core.log import get_logger

log = get_logger("db")


class ConnectionPool(object):
    pool: asyncpg.pool.Pool = None

    @staticmethod
    async def init(cfg, tries=10, interval=5):
        dsn = f'postgres://{cfg.db.user}:foobar@{cfg.db.host}:{cfg.db.port}/{cfg.db.name}'
        for _ in range(tries):
            try:
                ConnectionPool.pool = await asyncpg.create_pool(
                    dsn=dsn
                )
                log.info("Database connection established succesfully")
                return
            # tODO: catch more precise exception
            except Exception as e:
                log.warning("Unable to connect to database, retrying in %ss", interval)
            await asyncio.sleep(interval)
        raise RuntimeError("Could not connect to database")

    @staticmethod
    def acquire_connection() -> asyncpg.Connection:
        return ConnectionPool.pool.acquire()
        