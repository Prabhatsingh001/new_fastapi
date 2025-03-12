from fastapi.security import HTTPBearer
from fastapi import Request


class AcessTokenBearer(HTTPBearer):

    def __init__(self, auto_error = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        creds =  await super().__call__(request)

        print(creds.scheme)

        print(creds.credentials)

        return creds