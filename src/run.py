import signal
import os
import uvloop
import asyncio
import aiomisc
from core import config
from core.log import get_logger
from core.db import ConnectionPool
from service import ApiService

log = get_logger("core.run")

log.info("Loading config")
config = config.Config("./cfg/config.json")
log.info("Config loaded")

@aiomisc.receiver(aiomisc.entrypoint.PRE_START)
async def pre_init(entrypoint, services):
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
    await ConnectionPool.init(config)


log.info("Creating api service instance")
api = ApiService(config)
log.info("Api service instance created")

log.info("Installing uvloop")
uvloop.install()

try:
    with aiomisc.entrypoint(api, log_config=False) as loop:
        loop.run_forever()
except asyncio.CancelledError:
    pass

log.info("Application finished")
