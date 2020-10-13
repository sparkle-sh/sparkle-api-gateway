import enum
import sanic
import httpx


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
}


class Proxy(object):
    def __init__(self, name, host, port):
        self.name = name
        self.base_url = f'http://{host}:{port}'
        self.proxy = sanic.Blueprint(name, url_prefix=f'/{name}')

    def get(self, url):
        @self.proxy.get(url)
        async def proxy(req):
            return await self.handle_request(req, f'{self.base_url}{url}', Http.GET)

    def post(self, url):
        @self.proxy.post(url)
        async def proxy(req):
            return await self.handle_request(req, f'{self.base_url}{url}', Http.POST)

    def put(self, url):
        @self.proxy.put(url)
        async def proxy(req):
            return await self.handle_request(req, f'{self.base_url}{url}', Http.PUT)

    async def handle_request(self, req, url, method):
        r = None
        async with httpx.AsyncClient() as client:
            r = await HTTPX_REQUESTS[method](client, url)

        return sanic.response.json(
            r.json(),
            headers=r.headers,
            status=r.status_code
        )

    def get_sanic_blueprint(self) -> sanic.Blueprint:
        return self.proxy
