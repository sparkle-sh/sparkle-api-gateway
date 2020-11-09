import sanic
import httpx
import json
from sanic_jwt import protected
from core.log import get_logger

log = get_logger("proxy.midpoint_proxy")


def setup_midpoint_proxy(midpoint_cfg) -> sanic.Blueprint:
    log.info("Setting up midpoint proxy")
    midpoint_blueprints = []
    base_url = f'http://{midpoint_cfg.host}:{midpoint_cfg.port}'

    midpoint_blueprints.append(setup_root_proxy(base_url))
    midpoint_blueprints.append(setup_agent_proxy(base_url))
    midpoint_blueprints.append(setup_device_proxy(base_url))
    midpoint_blueprints.append(setup_task_proxy(base_url))

    return midpoint_blueprints


def setup_root_proxy(base_url) -> sanic.Blueprint:
    log.info("Setting up root proxy")
    bp = sanic.Blueprint('midpoint', url_prefix='/midpoint')

    @bp.get("/")
    @protected()
    async def root_get(req):
        headers = {
            "Authorization": req.headers["authorization"],
        }
        res = None
        try:
            async with httpx.AsyncClient() as client:
                res = await httpx.AsyncClient.get(client, f'{base_url}/', headers=headers)
        except httpx.ConnectError as e:
            log.warning(f"Could not handle request: {e}")
            return sanic.response.json({
                "msg": "Proxy endpoint provider is down"
            }, status=400)
        return sanic.response.json(
            res.json(),
            headers=res.headers,
            status=res.status_code
        )
    return bp


def setup_agent_proxy(base_url) -> sanic.Blueprint:
    log.info("Setting up agent proxy")
    bp = sanic.Blueprint('agent', url_prefix='/midpoint/agent')

    @bp.post("/")
    @protected()
    async def agent_post(req):
        headers = {
            "Authorization": req.headers["authorization"],
        }
        res = None
        try:
            async with httpx.AsyncClient() as client:
                res = await httpx.AsyncClient.post(client, f'{base_url}/agent', headers=headers)
        except httpx.ConnectError as e:
            log.warning(f"Could not handle request: {e}")
            return sanic.response.json({
                "msg": "Proxy endpoint provider is down"
            }, status=400)
        return sanic.response.json(
            res.json(),
            headers=res.headers,
            status=res.status_code
        )

    @bp.delete("/")
    @protected()
    async def agent_delete(req):
        headers = {
            "Authorization": req.headers["authorization"],
            "Agent-ID": req.headers["agent-ID"]
        }
        res = None
        try:
            async with httpx.AsyncClient() as client:
                res = await httpx.AsyncClient.delete(client, f'{base_url}/agent', headers=headers)
        except httpx.ConnectError as e:
            log.warning(f"Could not handle request: {e}")
            return sanic.response.json({
                "msg": "Proxy endpoint provider is down"
            }, status=400)
        return sanic.response.json(
            res.json(),
            headers=res.headers,
            status=res.status_code
        )

    return bp


def setup_device_proxy(base_url) -> sanic.Blueprint:
    log.info("Setting up device proxy")
    bp = sanic.Blueprint('device', url_prefix='/midpoint/device')

    @bp.get("/")
    @protected()
    async def device_get(req):
        headers = {
            "Authorization": req.headers["authorization"],
            "Agent-ID": req.headers["agent-ID"]
        }
        res = None
        try:
            async with httpx.AsyncClient() as client:
                res = await httpx.AsyncClient.get(client, f'{base_url}/device', headers=headers)
        except httpx.ConnectError as e:
            log.warning(f"Could not handle request: {e}")
            return sanic.response.json({
                "msg": "Proxy endpoint provider is down"
            }, status=400)
        return sanic.response.json(
            res.json(),
            headers=res.headers,
            status=res.status_code
        )

    @bp.get("/<id>/state")
    @protected()
    async def device_state_get(req, id: str):
        headers = {
            "Authorization": req.headers["authorization"],
            "Agent-ID": req.headers["agent-ID"]
        }
        res = None
        try:
            async with httpx.AsyncClient() as client:
                res = await httpx.AsyncClient.get(client, f'{base_url}/device/{id}/state', headers=headers)
        except httpx.ConnectError as e:
            log.warning(f"Could not handle request: {e}")
            return sanic.response.json({
                "msg": "Proxy endpoint provider is down"
            }, status=400)
        return sanic.response.json(
            res.json(),
            headers=res.headers,
            status=res.status_code
        )

    @bp.put("/<id>/state")
    @protected()
    async def device_state_put(req, id: str):
        headers = {
            "Authorization": req.headers["authorization"],
            "Agent-ID": req.headers["agent-ID"]
        }
        res = None
        try:
            async with httpx.AsyncClient() as client:
                res = await httpx.AsyncClient.put(client, f'{base_url}/device/{id}/state', headers=headers, json=req.json)
        except httpx.ConnectError as e:
            log.warning(f"Could not handle request: {e}")
            return sanic.response.json({
                "msg": "Proxy endpoint provider is down"
            }, status=400)
        return sanic.response.json(
            res.json(),
            headers=res.headers,
            status=res.status_code
        )

    @bp.get("/<id>/datasheet")
    @protected()
    async def device_datasheet_get(req, id: str):
        headers = {
            "Authorization": req.headers["authorization"],
            "Agent-ID": req.headers["agent-ID"]
        }
        res = None
        try:
            async with httpx.AsyncClient() as client:
                res = await httpx.AsyncClient.get(client, f'{base_url}/device/{id}/datasheet', headers=headers)
        except httpx.ConnectError as e:
            log.warning(f"Could not handle request: {e}")
            return sanic.response.json({
                "msg": "Proxy endpoint provider is down"
            }, status=400)
        return sanic.response.json(
            res.json(),
            headers=res.headers,
            status=res.status_code
        )

    @bp.get("/<id>/value/<label>")
    @protected()
    async def device_value_get(req, id: str, label: str):
        headers = {
            "Authorization": req.headers["authorization"],
            "Agent-ID": req.headers["agent-ID"]
        }
        res = None
        try:
            async with httpx.AsyncClient() as client:
                res = await httpx.AsyncClient.get(client, f'{base_url}/device/{id}/value/{label}', headers=headers)
        except httpx.ConnectError as e:
            log.warning(f"Could not handle request: {e}")
            return sanic.response.json({
                "msg": "Proxy endpoint provider is down"
            }, status=400)
        return sanic.response.json(
            res.json(),
            headers=res.headers,
            status=res.status_code
        )

    return bp


def setup_task_proxy(base_url) -> sanic.Blueprint:
    log.info("Setting up task proxy")
    bp = sanic.Blueprint('task', url_prefix='/midpoint/task')

    @bp.get("/")
    @protected()
    async def task_get(req):
        headers = {
            "Authorization": req.headers["authorization"],
            "Agent-ID": req.headers["agent-ID"]
        }
        res = None
        try:
            async with httpx.AsyncClient() as client:
                res = await httpx.AsyncClient.get(client, f'{base_url}/task', headers=headers)
        except httpx.ConnectError as e:
            log.warning(f"Could not handle request: {e}")
            return sanic.response.json({
                "msg": "Proxy endpoint provider is down"
            }, status=400)
        return sanic.response.json(
            res.json(),
            headers=res.headers,
            status=res.status_code
        )

    @bp.post("/")
    @protected()
    async def task_post(req):
        headers = {
            "Authorization": req.headers["authorization"],
            "Agent-ID": req.headers["agent-ID"]
        }
        res = None
        try:
            async with httpx.AsyncClient() as client:
                res = await httpx.AsyncClient.post(client, f'{base_url}/task', headers=headers, json=req.json)
        except httpx.ConnectError as e:
            log.warning(f"Could not handle request: {e}")
            return sanic.response.json({
                "msg": "Proxy endpoint provider is down"
            }, status=400)
        return sanic.response.json(
            res.json(),
            headers=res.headers,
            status=res.status_code
        )

    @bp.delete("/")
    @protected()
    async def task_delete(req):
        headers = {
            "Authorization": req.headers["authorization"],
            "Agent-ID": req.headers["agent-ID"]
        }
        res = None
        try:
            async with httpx.AsyncClient() as client:
                res = await httpx.AsyncClient.delete(client, f'{base_url}/task', headers=headers)
        except httpx.ConnectError as e:
            log.warning(f"Could not handle request: {e}")
            return sanic.response.json({
                "msg": "Proxy endpoint provider is down"
            }, status=400)
        return sanic.response.json(
            res.json(),
            headers=res.headers,
            status=res.status_code
        )

    @bp.put("/")
    @protected()
    async def task_put(req):
        headers = {
            "Authorization": req.headers["authorization"],
            "Agent-ID": req.headers["agent-ID"]
        }
        res = None
        try:
            async with httpx.AsyncClient() as client:
                res = await httpx.AsyncClient.put(client, f'{base_url}/task', headers=headers, json=req.json)
        except httpx.ConnectError as e:
            log.warning(f"Could not handle request: {e}")
            return sanic.response.json({
                "msg": "Proxy endpoint provider is down"
            }, status=400)
        return sanic.response.json(
            res.json(),
            headers=res.headers,
            status=res.status_code
        )

    return bp
