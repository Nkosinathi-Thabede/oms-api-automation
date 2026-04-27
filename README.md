# OMS API Automation Framework

API automation framework for an Order Management System (OMS), built as part of a QA Software Test Engineer assessment.

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.12 | Core language |
| pytest | Test runner |
| requests | HTTP client |
| Flask | Local mock OMS API server |
| PyJWT | JWT token generation |
| pytest-html | HTML report generation |
| GitHub Actions | CI/CD pipeline |

---

## Project Structure

```
oms-api-automation/
├── framework/
│   ├── auth/token_manager.py         # JWT generation + expired token helper
│   ├── client/api_client.py          # Reusable HTTP client
│   ├── validators/response_validator.py  # Chainable assertion helpers
│   └── utils/logger.py               # Logging setup
├── mock_server/server.py             # Flask mock OMS API
├── tests/
│   ├── test_create_order.py          # POST /orders — 15 tests
│   ├── test_get_order.py             # GET /orders/{id} — 11 tests
│   └── test_update_order_status.py   # PUT /orders/{id}/status — 16 tests
├── test_data/order_payloads.py       # Centralised test data
├── conftest.py                       # Shared fixtures
├── pytest.ini                        # Pytest config
└── .github/workflows/ci.yml         # GitHub Actions CI
```

---

## Running Locally

### 1. Clone and enter the project
```bash
git clone https://github.com/Nkosinathi-Thabede/oms-api-automation.git
cd oms-api-automation
```

### 2. Create virtual environment
```bash
python3 -m venv venv
source venv/bin/activate       # Mac/Linux
# venv\Scripts\activate        # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the tests
```bash
pytest
```

The mock server starts automatically — no external API or credentials needed.

### 5. View the HTML report
```
open reports/report.html
```

---

## Sample API Payloads

### POST /orders
```json
{
  "customer_id": "CUST-001",
  "items": [{ "sku": "ITEM-A", "quantity": 2, "price": 49.99 }],
  "shipping_address": {
    "line1": "123 Main St", "city": "Cape Town",
    "postal_code": "8001", "country": "ZA"
  }
}
```

### PUT /orders/{order_id}/status
```json
{ "status": "CONFIRMED" }
```

Valid statuses: `PENDING` → `CONFIRMED` → `PROCESSING` → `SHIPPED` → `DELIVERED` / `CANCELLED`

---

## Test Coverage

| Suite | Tests | Scope |
|-------|-------|-------|
| Create Order | 15 | Happy path, missing fields, invalid values, auth |
| Get Order | 11 | Happy path, not found, auth |
| Update Status | 16 | Valid transitions, invalid values, terminal states, auth |
| **Total** | **42** | |
