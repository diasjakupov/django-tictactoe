from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async
from django.contrib.auth.models import User

@database_sync_to_async
def get_user(id):
    return User.objects.get(pk=int(id))

class TokenAuthMiddleWare(BaseMiddleware):
    def __init__(self, inner):
        super().__init__(inner)

    async def __call__(self, scope, receive, send):
        try:
            print("Middleware")
            id = scope["query_string"].decode()
            id = id.replace("id=", "")
            print("good try")
        except Exception as e:
            print(e)
            id = "", ""

        if id != "":
            try:
                user = await get_user(id)
            except Exception as e:
                user = None
                print(e)
            scope["user"]=user
        else:
            scope["user"]=None
        return await super().__call__(scope, receive, send)