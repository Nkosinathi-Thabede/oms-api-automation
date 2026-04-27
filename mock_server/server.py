from flask import Flask, request, jsonify
import uuid
import time
import jwt

app = Flask(__name__)
SECRET = "oms-test-secret-key"
ALGORITHM = "HS256"
VALID_STATUSES = ["PENDING", "CONFIRMED", "PROCESSING", "SHIPPED", "DELIVERED", "CANCELLED"]
orders: dict = {}


def verify_token(req):
    auth = req.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        return False, "Missing or malformed Authorization header"
    token = auth.split(" ", 1)[1]
    try:
        jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        return True, ""
    except jwt.ExpiredSignatureError:
        return False, "Token has expired"
    except jwt.InvalidTokenError as e:
        return False, str(e)


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


@app.route("/orders", methods=["POST"])
def create_order():
    ok, err = verify_token(request)
    if not ok:
        return jsonify({"error": err}), 401
    body = request.get_json(silent=True)
    if not body:
        return jsonify({"error": "Request body is required"}), 400
    missing = [f for f in ["customer_id", "items", "shipping_address"] if f not in body]
    if missing:
        return jsonify({"error": f"Missing required fields: {missing}"}), 400
    if not isinstance(body["items"], list) or len(body["items"]) == 0:
        return jsonify({"error": "items must be a non-empty list"}), 400
    for item in body["items"]:
        if "sku" not in item or "quantity" not in item or "price" not in item:
            return jsonify({"error": "Each item requires sku, quantity, and price"}), 400
        if item["quantity"] <= 0:
            return jsonify({"error": "Item quantity must be greater than zero"}), 422
        if item["price"] < 0:
            return jsonify({"error": "Item price cannot be negative"}), 422
    order_id = f"ORD-{uuid.uuid4().hex[:8].upper()}"
    total = sum(i["quantity"] * i["price"] for i in body["items"])
    order = {
        "order_id": order_id,
        "customer_id": body["customer_id"],
        "items": body["items"],
        "shipping_address": body["shipping_address"],
        "status": "PENDING",
        "total": round(total, 2),
        "created_at": int(time.time())
    }
    orders[order_id] = order
    return jsonify(order), 201


@app.route("/orders/<order_id>", methods=["GET"])
def get_order(order_id):
    ok, err = verify_token(request)
    if not ok:
        return jsonify({"error": err}), 401
    order = orders.get(order_id)
    if not order:
        return jsonify({"error": f"Order {order_id} not found"}), 404
    return jsonify(order), 200


@app.route("/orders/<order_id>/status", methods=["PUT"])
def update_order_status(order_id):
    ok, err = verify_token(request)
    if not ok:
        return jsonify({"error": err}), 401
    order = orders.get(order_id)
    if not order:
        return jsonify({"error": f"Order {order_id} not found"}), 404
    body = request.get_json(silent=True)
    if not body or "status" not in body:
        return jsonify({"error": "Field 'status' is required"}), 400
    new_status = body["status"].upper()
    if new_status not in VALID_STATUSES:
        return jsonify({"error": f"Invalid status '{new_status}'. Valid: {VALID_STATUSES}"}), 422
    if order["status"] == "DELIVERED" and new_status != "DELIVERED":
        return jsonify({"error": "Cannot update status of a delivered order"}), 409
    if order["status"] == "CANCELLED":
        return jsonify({"error": "Cannot update status of a cancelled order"}), 409
    order["status"] = new_status
    orders[order_id] = order
    return jsonify(order), 200


if __name__ == "__main__":
    app.run(port=5050, debug=False)
