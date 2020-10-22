from sanic_jwt import exceptions
from core.db import ConnectionPool
import bcrypt
from core.log import get_logger

log = get_logger("auth.auth")

async def authenticate(request, *args, **kwargs):
    log.debug("Starting authentication process")
    if not request.json:
        raise exceptions.AuthenticationFailed("Body is required")
    if 'username' not in request.json:
        raise exceptions.AuthenticationFailed("Username is required")
    username = request.json.get('username') 
    if 'passwd' not in request.json:
        raise exceptions.AuthenticationFailed("Passwd is required")
    passwd = request.json.get('passwd')

    async with ConnectionPool.acquire_connection() as conn:
        log.debug("Aquiring db connection")
        query = f"SELECT passwd FROM users WHERE name='{username}'"
        res = await conn.fetch(query)
        if not res:
            raise exceptions.AuthenticationFailed("Invalid username")
        if not bcrypt.checkpw(passwd.encode(),res[0]['passwd'].encode()):
            raise exceptions.AuthenticationFailed("Invalid password")

    user = {'username': username, 'passwd': passwd}
    log.debug(f"User with username {username} has been authenticated")
    return user



    