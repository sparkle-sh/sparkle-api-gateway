import json
import asyncio
import aiomisc
import sanic
from core.log import get_logger
from proxy import setup_proxies
from sanic_jwt import initialize
from sanic_jwt import protected
from auth import auth


log = get_logger("service")


class ApiService(aiomisc.Service):
    def __init__(self, cfg):
        self.cfg = cfg
        self.app = sanic.Sanic(name='sparkle-api-gateway')

    async def start(self):
        log.info("Starting api service")
        initialize(self.app, url_prefix = '/login', authenticate=auth.authenticate)
        self.setup_root_endpoints()
        setup_proxies(self.app, self.cfg)
        await asyncio.create_task(
            self.app.create_server(host=self.cfg.api.host, port=self.cfg.api.port, return_asyncio_server=True))

    async def stop(self, exception: Exception = None):
        log.info("Stopping api service")

    def setup_root_endpoints(self):
        @self.app.get("/")
        @protected()
        async def root_endpoint(req):
            return sanic.response.json(self.get_application_info())

        @self.app.exception(sanic.exceptions.NotFound)
        async def handle_404(request, exception):
            log.warning(f"Route {request.url} not found")
            return sanic.response.json({
                "msg": f"Route {request.url} not found"}, status=404)

        @self.app.exception(sanic.exceptions.InvalidUsage)
        async def handle_invalid_usage(request, exception):
            log.warning(f"Invalid request body format {request.body}")
            return sanic.response.json({
                "msg": f"Invalid body format"}, status=400)

        @self.app.exception(sanic.exceptions.MethodNotSupported)
        async def handle_invalid_method(request, exception):
            log.warning(f"Method {request.method} not allowed for url {request.url}")
            return sanic.response.json({
                "msg": f"Method {request.method} not allowed for url {request.url}"}, status=405)

    def get_application_info(self):
        payload = {
            'name': 'sparkle-api-gateway'
        }

        with open('./version.json', 'r') as f:
            payload["version"] = json.loads(f.read())

        return payload
