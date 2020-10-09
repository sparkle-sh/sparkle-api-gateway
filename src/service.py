import json
import asyncio
import aiomisc
import sanic
from core.log import get_logger


log = get_logger("api")
HOST = '127.0.0.1'
PORT = 7776


class ApiService(aiomisc.Service):
    def __init__(self):
        self.host = HOST
        self.port = PORT
        self.app = sanic.Sanic(name='sparkle-midpoint')
    
    async def start(self):
        log.info("Starting api service")

        await self.setup_root_endpoint()
        await asyncio.create_task(
            self.app.create_server(host=self.host, port=self.port, return_asyncio_server=True))

    async def stop(self, exception: Exception = None):
        log.info("Stopping api service")

    async def setup_root_endpoint(self):
        @self.app.get("/")
        async def root_endpoint(req):
            return sanic.response.json(self.get_application_info())

    def get_application_info(self):
        payload = {
            'name': 'sparkle-api-gateway'
        }

        with open('./version.json', 'r') as f:
            payload["version"] = json.loads(f.read())

        return payload
