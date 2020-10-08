import signal
import os
import uvloop
import asyncio
import aiomisc
from core.log import get_logger


log = get_logger("main")


@aiomisc.receiver(aiomisc.entrypoint.PRE_START)
async def pre_init(entrypoint, services) -> None:
    log = get_logger("main.init")

    log.info("setting up signal handler")

    async def shutdown() -> None:
        log.info("received SIGINT/SIGTERM shutting down all active task")
        tasks = [t for t in asyncio.Task.all_tasks(
        ) if t is not asyncio.Task.current_task()]
        for task in tasks:
            task.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)
        log.info("stopping event loop")
        asyncio.get_event_loop().stop()

    for sig in [signal.SIGTERM, signal.SIGINT]:
        asyncio.get_event_loop().add_signal_handler(
            sig, lambda: asyncio.create_task(shutdown())
        )


print("Hello API!")
