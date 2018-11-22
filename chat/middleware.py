import requests, json


class TokenAuthMiddleware:

    def __init__(self, inner):
        # Store the ASGI application we were passed
        self.inner = inner

    def __call__(self, scope):
        # override the call with scope passed in
        access_token_name, access_token_string = scope['query_string'].decode().split("=")
        response = requests.get("http://trader-flask-nz.herokuapp.com/users/account", headers={
           'X-Auth': access_token_string})
        return self.inner(dict(scope, user=response.text))
