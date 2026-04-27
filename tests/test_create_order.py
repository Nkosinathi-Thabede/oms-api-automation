"""
Test Suite: Create Order — POST /orders
Covers: happy path, missing fields, invalid values, authentication
"""
import pytest
from framework.validators.response_validator import ResponseValidator
from framework.auth.token_manager import TokenManager
from test_data.order_payloads import (
    VALID_ORDER, VALID_ORDER_MULTI_ITEM, VALID_ORDER_SINGLE_ITEM,
    MISSING_CUSTOMER_ID, MISSING_ITEMS, MISSING_SHIPPING_ADDRESS,
    EMPTY_ITEMS_LIST, ZERO_QUANTITY, NEGATIVE_PRICE
)


class TestCreateOrderHappyPath:

    def test_create_order_returns_201(self, client):
        response = client.post("/orders", VALID_ORDER)
        ResponseValidator(response).status_is(201)

    def test_create_order_returns_order_id(self, client):
        response = client.post("/orders", VALID_ORDER)
        ResponseValidator(response).status_is(201).has_field("order_id").field_not_empty("order_id")

    def test_create_order_status_is_pending(self, client):
        response = client.post("/orders", VALID_ORDER)
        ResponseValidator(response).status_is(201).field_equals("status", "PENDING")

    def test_create_order_total_is_calculated(self, client):
        response = client.post("/orders", VALID_ORDER)
        body = response.json()
        expected_total = sum(i["quantity"] * i["price"] for i in VALID_ORDER["items"])
        assert round(body["total"], 2) == round(expected_total, 2)

    def test_create_order_returns_all_required_fields(self, client):
        response = client.post("/orders", VALID_ORDER)
        ResponseValidator(response).has_fields(
            "order_id", "customer_id", "items",
            "shipping_address", "status", "total", "created_at"
        )

    def test_create_order_response_is_json(self, client):
        response = client.post("/orders", VALID_ORDER)
        ResponseValidator(response).content_type_is_json()

    @pytest.mark.parametrize("payload,label", [
        (VALID_ORDER, "single_item"),
        (VALID_ORDER_MULTI_ITEM, "multi_item"),
        (VALID_ORDER_SINGLE_ITEM, "minimum_order"),
    ])
    def test_create_order_data_driven(self, client, payload, label):
        response = client.post("/orders", payload)
        ResponseValidator(response).status_is(201).has_field("order_id")

    def test_create_order_multi_item_total_is_correct(self, client):
        response = client.post("/orders", VALID_ORDER_MULTI_ITEM)
        body = response.json()
        expected = sum(i["quantity"] * i["price"] for i in VALID_ORDER_MULTI_ITEM["items"])
        assert round(body["total"], 2) == round(expected, 2)

    def test_each_order_gets_unique_id(self, client):
        r1 = client.post("/orders", VALID_ORDER)
        r2 = client.post("/orders", VALID_ORDER)
        assert r1.json()["order_id"] != r2.json()["order_id"]


class TestCreateOrderMissingFields:

    @pytest.mark.parametrize("payload,missing_field", [
        (MISSING_CUSTOMER_ID, "customer_id"),
        (MISSING_ITEMS, "items"),
        (MISSING_SHIPPING_ADDRESS, "shipping_address"),
    ])
    def test_missing_required_field_returns_400(self, client, payload, missing_field):
        response = client.post("/orders", payload)
        ResponseValidator(response).status_is(400).has_field("error")

    def test_empty_body_returns_400(self, client):
        response = client.post("/orders", {})
        ResponseValidator(response).status_is(400)

    def test_no_body_returns_400(self, client):
        response = client.post("/orders", None)
        ResponseValidator(response).status_is(400)


class TestCreateOrderInvalidValues:

    def test_empty_items_list_returns_400(self, client):
        response = client.post("/orders", EMPTY_ITEMS_LIST)
        ResponseValidator(response).status_is(400).has_field("error")

    def test_zero_quantity_returns_422(self, client):
        response = client.post("/orders", ZERO_QUANTITY)
        ResponseValidator(response).status_is(422).has_field("error")

    def test_negative_price_returns_422(self, client):
        response = client.post("/orders", NEGATIVE_PRICE)
        ResponseValidator(response).status_is(422).has_field("error")


class TestCreateOrderAuthentication:

    def test_no_token_returns_401(self, client):
        response = client.without_token().post("/orders", VALID_ORDER)
        ResponseValidator(response).status_is(401)

    def test_expired_token_returns_401(self, client):
        expired_client = client.with_token(TokenManager().get_expired_token())
        response = expired_client.post("/orders", VALID_ORDER)
        ResponseValidator(response).status_is(401).error_message_contains("expired")

    def test_invalid_token_returns_401(self, client):
        response = client.with_token("this.is.not.valid").post("/orders", VALID_ORDER)
        ResponseValidator(response).status_is(401)
