from sanic_jwt import exceptions
from core.db import ConnectionPool


async def authenticate(request, *args, **kwargs):
    username = request.json.get('username', None) 
    passwd = request.json.get('passwd', None)

    async with ConnectionPool.acquire_connection() as conn:
        query = f"SELECT passwd FROM users WHERE name='{username}'"
        res = await conn.fetch(query)
        if not res:
            raise exceptions.AuthenticationFailed("Invalid username")
        
        if passwd != res[0]['passwd']:
            raise exceptions.AuthenticationFailed("Invalid password")

    user = {'username': username, 'passwd': passwd}
    return user



    