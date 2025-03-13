from fastapi.security import HTTPBearer
from fastapi import Request, status
from fastapi.security.http import HTTPAuthorizationCredentials
from src.auth.utils import decode_access_token
from fastapi.exceptions import HTTPException

class AcessTokenBearer(HTTPBearer):

    def __init__(self, auto_error = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials|None:
        creds =  await super().__call__(request)
        token = creds.credentials
        token_data = decode_access_token(token)
        if not self.token_valid:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="invalid or expired token")
        
        if token_data['refresh']:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="plss provide valid access token"
            )
        return token_data

    
    def token_valid(self,token: str) -> bool:
        token_data = decode_access_token(token)
        if token_data is not None:
            return True
        else:
            return False