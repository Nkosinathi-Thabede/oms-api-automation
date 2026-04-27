import requests
import logging

logger = logging.getLogger(__name__)


class APIClient:
    def __init__(self, base_url: str, token: str = None):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        if token:
            self.session.headers.update({
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
                "Accept": "application/json"
            })

    def _url(self, path: str) -> str:
        return f"{self.base_url}/{path.lstrip('/')}"

    def get(self, path: str, params: dict = None) -> requests.Response:
        return self.session.get(self._url(path), params=params)

    def post(self, path: str, payload: dict = None) -> requests.Response:
        return self.session.post(self._url(path), json=payload)

    def put(self, path: str, payload: dict = None) -> requests.Response:
        return self.session.put(self._url(path), json=payload)

    def delete(self, path: str) -> requests.Response:
        return self.session.delete(self._url(path))

    def with_token(self, token: str) -> "APIClient":
        return APIClient(base_url=self.base_url, token=token)

    def without_token(self) -> "APIClient":
        return APIClient(base_url=self.base_url, token=None)
