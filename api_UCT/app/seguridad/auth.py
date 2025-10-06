from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.config import SECRET_TOKEN

seguridad = HTTPBearer()

def verificar_token(credenciales: HTTPAuthorizationCredentials = Depends(seguridad)):
    if credenciales.credentials != SECRET_TOKEN:
        raise HTTPException(status_code=401, detail='Credenciales inválidas')
