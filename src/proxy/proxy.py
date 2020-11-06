import enum
import sanic
import httpx
from sanic_jwt import protected


class Http(enum.IntEnum):
    GET = 0
    POST = 1
    PUT = 2
    DELETE = 3
    UPDATE = 4


HTTPX_REQUESTS = {
    Http.GET: httpx.AsyncClient.get,
    Http.POST: httpx.AsyncClient.post,
    Http.PUT: httpx.AsyncClient.put,
    Http.DELETE: httpx.AsyncClient.delete
}


class Proxy(object):
    def __init__(self, name, host, port):
        self.name = name
        self.base_url = f'http://{host}:{port}'
        self.proxy = sanic.Blueprint(name, url_prefix=f'/{name}')

    def get(self, url):
        @self.proxy.get(url)
        @protected()
        async def proxy(req, *args):
            return await self.handle_request(req, f'{self.base_url}{url}', Http.GET)

    def post(self, url):
        @self.proxy.post(url)
        @protected()
        async def proxy(req, *args, **kwargs):
            return await self.handle_request(req, f'{self.base_url}{url}', Http.POST)

    def put(self, url):
        @self.proxy.put(url)
        @protected()
        async def proxy(req, *args):
            return await self.handle_request(req, f'{self.base_url}{url}', Http.PUT)

    def delete(self, url):
        @self.proxy.delete(url)
        @protected()
        async def proxy(req, *args):
            return await self.handle_request(req, f'{self.base_url}{url}', Http.DELETE)

    async def handle_request(self, req, url, method):
        r = None
        try:
            data = req.json if req.json is not None else {}
            headers = req.headers if req.headers is not None else {}
            async with httpx.AsyncClient() as client:
                if method == Http.GET:
                    r = await HTTPX_REQUESTS[method](client, url, headers=headers)
                else:
                    r = await HTTPX_REQUESTS[method](client, url, json=data)
        except httpx.ConnectError as e:
            log.warning(f"Could not handle request: {e}")
            return sanic.response.json({
                "msg": "Proxy endpoint provider is down"
            }, status=400)

        return sanic.response.json(
            r.json(),
            headers=r.headers,
            status=r.status_code
        )

    def get_sanic_blueprint(self) -> sanic.Blueprint:
        return self.proxy
