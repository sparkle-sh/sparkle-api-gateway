import sanic
import httpx
import json


async def setup_midpoint_proxy(midpoint_cfg) -> sanic.Blueprint:
    midpoint_proxy = sanic.Blueprint('midpoint', url_prefix='/midpoint')
    base_path = f'http://{midpoint_cfg.host}:{midpoint_cfg.port}/'

    @midpoint_proxy.get("/")
    async def midpoint_root(req):
        r = None
        async with httpx.AsyncClient() as c:
            r = await c.get(base_path)

        return sanic.response.json(
            r.json(),
            headers=r.headers,
            status=r.status_code
        )

    return midpoint_proxy
