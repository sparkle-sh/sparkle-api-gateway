import signal
import os
import uvloop
import asyncio
import aiomisc
from core.log import get_logger
from core.db import ConnectionPool


log = get_logger("main")


@aiomisc.receiver(aiomisc.entrypoint.PRE_START)
async def pre_init(entrypoint, services) -> None:
    log.info("Setting up signal handler")

    async def shutdown() -> None:
        log.info("Received SIGINT/SIGTERM shutting down all active task")
        tasks = [t for t in asyncio.Task.all_tasks(
        ) if t is not asyncio.Task.current_task()]
        for task in tasks:
            task.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)
        log.info("Stopping event loop")
        asyncio.get_event_loop().stop()

    for sig in [signal.SIGTERM, signal.SIGINT]:
        asyncio.get_event_loop().add_signal_handler(
            sig, lambda: asyncio.create_task(shutdown())
        )

    log.info("Connecting connection pool")
    await ConnectionPool.init()


async def main():
    async with ConnectionPool.acquire_connection() as conn:
        users = await conn.fetch("SELECT * from users")
        for user in users:
            print(user['name'], user['passwd'])

try:
    with aiomisc.entrypoint(log_config=False) as loop:
        loop.run_until_complete(main())
except asyncio.CancelledError:
    pass

log.info("Application finished")