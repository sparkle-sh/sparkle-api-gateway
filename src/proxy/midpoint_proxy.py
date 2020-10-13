import sanic
import httpx
import json
from proxy import proxy


async def setup_midpoint_proxy(midpoint_cfg) -> sanic.Blueprint:
    midpoint_proxy = proxy.Proxy(
        'midpoint', midpoint_cfg.host, midpoint_cfg.port)

    midpoint_proxy.get("/")
    midpoint_proxy.post("/")

    return midpoint_proxy.get_sanic_blueprint()
