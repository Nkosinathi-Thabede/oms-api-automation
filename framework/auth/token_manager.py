import jwt
import time

SECRET = "oms-test-secret-key"
ALGORITHM = "HS256"
TOKEN_TTL_SECONDS = 3600


class TokenManager:
    _cached_token: str = None
    _expires_at: float = 0

    def get_token(self) -> str:
        if self._cached_token and time.time() < self._expires_at - 60:
            return self._cached_token
        now = int(time.time())
        payload = {
            "sub": "qa-test-user",
            "iat": now,
            "exp": now + TOKEN_TTL_SECONDS,
            "roles": ["qa", "read", "write"]
        }
        self._cached_token = jwt.encode(payload, SECRET, algorithm=ALGORITHM)
        self._expires_at = now + TOKEN_TTL_SECONDS
        return self._cached_token

    def get_expired_token(self) -> str:
        payload = {
            "sub": "qa-test-user",
            "iat": int(time.time()) - 7200,
            "exp": int(time.time()) - 3600,
        }
        return jwt.encode(payload, SECRET, algorithm=ALGORITHM)
