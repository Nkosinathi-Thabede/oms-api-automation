"""
Test Suite: Update Order Status — PUT /orders/{order_id}/status
Covers: valid transitions, invalid values, terminal states, not found, authentication
"""
import pytest
from framework.validators.response_validator import ResponseValidator
from framework.auth.token_manager import TokenManager
from test_data.order_payloads import VALID_ORDER, VALID_STATUSES, INVALID_STATUSES


class TestUpdateOrderStatusHappyPath:

    def test_update_status_returns_200(self, client, created_order):
        response = client.put(f"/orders/{created_order['order_id']}/status", {"status": "CONFIRMED"})
        ResponseValidator(response).status_is(200)

    def test_update_status_reflects_new_status(self, client, created_order):
        order_id = created_order["order_id"]
        client.put(f"/orders/{order_id}/status", {"status": "CONFIRMED"})
        ResponseValidator(client.get(f"/orders/{order_id}")).field_equals("status", "CONFIRMED")

    @pytest.mark.parametrize("status", VALID_STATUSES)
    def test_all_valid_statuses_accepted(self, client, status):
        order = client.post("/orders", VALID_ORDER).json()
        response = client.put(f"/orders/{order['order_id']}/status", {"status": status})
        ResponseValidator(response).status_is(200).field_equals("status", status)

    def test_update_status_returns_full_order(self, client, created_order):
        response = client.put(f"/orders/{created_order['order_id']}/status", {"status": "PROCESSING"})
        ResponseValidator(response).has_fields("order_id", "customer_id", "items", "status", "total")

    def test_status_update_is_persisted(self, client, created_order):
        order_id = created_order["order_id"]
        client.put(f"/orders/{order_id}/status", {"status": "SHIPPED"})
        ResponseValidator(client.get(f"/orders/{order_id}")).field_equals("status", "SHIPPED")


class TestUpdateOrderStatusInvalidValues:

    @pytest.mark.parametrize("bad_status", INVALID_STATUSES)
    def test_invalid_status_returns_422(self, client, bad_status):
        order = client.post("/orders", VALID_ORDER).json()
        response = client.put(f"/orders/{order['order_id']}/status", {"status": bad_status})
        ResponseValidator(response).status_is(422).has_field("error")

    def test_missing_status_field_returns_400(self, client, created_order):
        response = client.put(f"/orders/{created_order['order_id']}/status", {})
        ResponseValidator(response).status_is(400).has_field("error")

    def test_empty_body_returns_400(self, client, created_order):
        response = client.put(f"/orders/{created_order['order_id']}/status", None)
        ResponseValidator(response).status_is(400)


class TestUpdateOrderTerminalStates:

    def test_cannot_update_delivered_order(self, client):
        order = client.post("/orders", VALID_ORDER).json()
        order_id = order["order_id"]
        client.put(f"/orders/{order_id}/status", {"status": "DELIVERED"})
        ResponseValidator(client.put(f"/orders/{order_id}/status", {"status": "PROCESSING"})).status_is(409)

    def test_cannot_update_cancelled_order(self, client):
        order = client.post("/orders", VALID_ORDER).json()
        order_id = order["order_id"]
        client.put(f"/orders/{order_id}/status", {"status": "CANCELLED"})
        ResponseValidator(client.put(f"/orders/{order_id}/status", {"status": "CONFIRMED"})).status_is(409)

    def test_delivered_order_keeps_status(self, client):
        order = client.post("/orders", VALID_ORDER).json()
        order_id = order["order_id"]
        client.put(f"/orders/{order_id}/status", {"status": "DELIVERED"})
        client.put(f"/orders/{order_id}/status", {"status": "PROCESSING"})
        ResponseValidator(client.get(f"/orders/{order_id}")).field_equals("status", "DELIVERED")


class TestUpdateOrderStatusNotFound:

    def test_nonexistent_order_returns_404(self, client):
        response = client.put("/orders/ORD-GHOST999/status", {"status": "CONFIRMED"})
        ResponseValidator(response).status_is(404).has_field("error")


class TestUpdateOrderStatusAuthentication:

    def test_no_token_returns_401(self, client, created_order):
        response = client.without_token().put(f"/orders/{created_order['order_id']}/status", {"status": "CONFIRMED"})
        ResponseValidator(response).status_is(401)

    def test_expired_token_returns_401(self, client, created_order):
        expired_client = client.with_token(TokenManager().get_expired_token())
        response = expired_client.put(f"/orders/{created_order['order_id']}/status", {"status": "CONFIRMED"})
        ResponseValidator(response).status_is(401)
