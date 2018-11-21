import requests, json


class TokenAuthMiddleware:

    def __init__(self, inner):
        # Store the ASGI application we were passed
        self.inner = inner

    def __call__(self, scope):
        # override the call with scope passed in
        token = str(dict(scope['headers'])[b'cookie']).split(";")[2].split("=")[1].strip("'")
        response = requests.get("http://localhost:5000/users/account", headers={
            'X-Auth': "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJrZXkiOjIsImlhdCI6MTU0MjgxMTA0NH0.NruUYbFo3iixgTn0TsLmXU-rX2hIsTgTOMueEY_Recg"})
        return self.inner(dict(scope, user=response.text))
