from requests import Response


class ResponseValidator:
    def __init__(self, response: Response):
        self.response = response
        self.body = self._parse_body()

    def _parse_body(self) -> dict:
        try:
            return self.response.json()
        except Exception:
            return {}

    def status_is(self, expected: int) -> "ResponseValidator":
        actual = self.response.status_code
        assert actual == expected, f"Expected status {expected}, got {actual}. Body: {self.response.text[:300]}"
        return self

    def has_field(self, field: str) -> "ResponseValidator":
        assert field in self.body, f"Expected field '{field}' in response. Got: {list(self.body.keys())}"
        return self

    def field_equals(self, field: str, expected) -> "ResponseValidator":
        self.has_field(field)
        assert self.body[field] == expected, f"Expected '{field}'={expected!r}, got {self.body[field]!r}"
        return self

    def field_not_empty(self, field: str) -> "ResponseValidator":
        self.has_field(field)
        assert self.body[field], f"Expected '{field}' to be non-empty"
        return self

    def has_fields(self, *fields: str) -> "ResponseValidator":
        for field in fields:
            self.has_field(field)
        return self

    def content_type_is_json(self) -> "ResponseValidator":
        ct = self.response.headers.get("Content-Type", "")
        assert "application/json" in ct, f"Expected JSON content type, got: {ct}"
        return self

    def error_message_contains(self, substring: str) -> "ResponseValidator":
        message = self.body.get("error") or self.body.get("message") or str(self.body)
        assert substring.lower() in message.lower(), f"Expected error containing '{substring}', got: {message}"
        return self
