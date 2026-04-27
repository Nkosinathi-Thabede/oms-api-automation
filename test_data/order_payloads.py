"""
Centralised test data — keeps payloads out of test files for easy maintenance.
"""

VALID_ORDER = {
    "customer_id": "CUST-001",
    "items": [{"sku": "ITEM-A", "quantity": 2, "price": 49.99}],
    "shipping_address": {
        "line1": "123 Main St",
        "city": "Cape Town",
        "postal_code": "8001",
        "country": "ZA"
    }
}

VALID_ORDER_MULTI_ITEM = {
    "customer_id": "CUST-002",
    "items": [
        {"sku": "ITEM-A", "quantity": 1, "price": 29.99},
        {"sku": "ITEM-B", "quantity": 3, "price": 15.00},
        {"sku": "ITEM-C", "quantity": 1, "price": 99.99},
    ],
    "shipping_address": {
        "line1": "456 Long St",
        "city": "Johannesburg",
        "postal_code": "2000",
        "country": "ZA"
    }
}

VALID_ORDER_SINGLE_ITEM = {
    "customer_id": "CUST-003",
    "items": [{"sku": "ITEM-Z", "quantity": 1, "price": 9.99}],
    "shipping_address": {
        "line1": "1 Beach Rd",
        "city": "Durban",
        "postal_code": "4001",
        "country": "ZA"
    }
}

MISSING_CUSTOMER_ID = {
    "items": [{"sku": "ITEM-A", "quantity": 1, "price": 10.00}],
    "shipping_address": {"line1": "123 St", "city": "CT", "postal_code": "8001", "country": "ZA"}
}

MISSING_ITEMS = {
    "customer_id": "CUST-001",
    "shipping_address": {"line1": "123 St", "city": "CT", "postal_code": "8001", "country": "ZA"}
}

MISSING_SHIPPING_ADDRESS = {
    "customer_id": "CUST-001",
    "items": [{"sku": "ITEM-A", "quantity": 1, "price": 10.00}]
}

EMPTY_ITEMS_LIST = {
    "customer_id": "CUST-001",
    "items": [],
    "shipping_address": {"line1": "123 St", "city": "CT", "postal_code": "8001", "country": "ZA"}
}

ZERO_QUANTITY = {
    "customer_id": "CUST-001",
    "items": [{"sku": "ITEM-A", "quantity": 0, "price": 10.00}],
    "shipping_address": {"line1": "123 St", "city": "CT", "postal_code": "8001", "country": "ZA"}
}

NEGATIVE_PRICE = {
    "customer_id": "CUST-001",
    "items": [{"sku": "ITEM-A", "quantity": 1, "price": -5.00}],
    "shipping_address": {"line1": "123 St", "city": "CT", "postal_code": "8001", "country": "ZA"}
}

VALID_STATUSES = ["CONFIRMED", "PROCESSING", "SHIPPED", "DELIVERED"]
INVALID_STATUSES = ["DISPATCHED", "UNKNOWN", "123"]
