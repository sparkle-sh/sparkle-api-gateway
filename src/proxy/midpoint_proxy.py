import sanic
import httpx
import json
from proxy import proxy


def setup_midpoint_proxy(midpoint_cfg) -> sanic.Blueprint:
    midpoint_proxy = proxy.Proxy(
        'midpoint', midpoint_cfg.host, midpoint_cfg.port)

    midpoint_proxy.get("/")

    return midpoint_proxy.get_sanic_blueprint()
