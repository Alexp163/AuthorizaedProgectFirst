from fastapi import HTTPException, status

import jwt

secret_key = "ijasfdioj83rj89jafsd83jaf8"
algorithm = "HS256"

class CredentialsRepository:
    def make_token(self, user_id: int) -> str:
        payload = {
            "user_id": user_id,
        }
        token = jwt.encode(payload, secret_key, algorithm)
        return token

    def valid_and_decode_token(self, token: str) -> int: # в токене зашит user_id
        try:
            payload = jwt.decode(token, secret_key, [algorithm])
            print(type(payload), payload)
            return payload["user_id"]
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Срок действия токена истек")
        except Exception:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Отказано в доступе")
