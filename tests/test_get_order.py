"""
Test Suite: Get Order — GET /orders/{order_id}
Covers: happy path, not found, authentication
"""
from framework.validators.response_validator import ResponseValidator
from framework.auth.token_manager import TokenManager


class TestGetOrderHappyPath:

    def test_get_order_returns_200(self, client, created_order):
        response = client.get(f"/orders/{created_order['order_id']}")
        ResponseValidator(response).status_is(200)

    def test_get_order_returns_correct_id(self, client, created_order):
        order_id = created_order["order_id"]
        response = client.get(f"/orders/{order_id}")
        ResponseValidator(response).status_is(200).field_equals("order_id", order_id)

    def test_get_order_returns_all_fields(self, client, created_order):
        response = client.get(f"/orders/{created_order['order_id']}")
        ResponseValidator(response).has_fields(
            "order_id", "customer_id", "items",
            "shipping_address", "status", "total", "created_at"
        )

    def test_get_order_status_is_pending_on_creation(self, client, created_order):
        response = client.get(f"/orders/{created_order['order_id']}")
        ResponseValidator(response).field_equals("status", "PENDING")

    def test_get_order_response_is_json(self, client, created_order):
        response = client.get(f"/orders/{created_order['order_id']}")
        ResponseValidator(response).content_type_is_json()

    def test_get_order_items_are_preserved(self, client, created_order):
        response = client.get(f"/orders/{created_order['order_id']}")
        assert len(response.json()["items"]) == len(created_order["items"])


class TestGetOrderNotFound:

    def test_nonexistent_order_returns_404(self, client):
        ResponseValidator(client.get("/orders/ORD-DOESNOTEXIST")).status_is(404).has_field("error")

    def test_random_id_returns_404(self, client):
        ResponseValidator(client.get("/orders/ORD-00000000")).status_is(404)

    def test_404_response_contains_error_field(self, client):
        ResponseValidator(client.get("/orders/ORD-FAKE999")).status_is(404).has_field("error")


class TestGetOrderAuthentication:

    def test_no_token_returns_401(self, client, created_order):
        response = client.without_token().get(f"/orders/{created_order['order_id']}")
        ResponseValidator(response).status_is(401)

    def test_expired_token_returns_401(self, client, created_order):
        expired_client = client.with_token(TokenManager().get_expired_token())
        response = expired_client.get(f"/orders/{created_order['order_id']}")
        ResponseValidator(response).status_is(401)
