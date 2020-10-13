from sanic_jwt import exceptions


async def authenticate(request, *args, **kwargs):
    username = request.json.get('username', None) 
    passwd = request.json.get('passwd', None)

    if not username or not passwd:
        raise exceptions.AuthenticationFailed("Missing username or password")
    
    user = {'username': username, 'passwd': passwd}
    return user



    