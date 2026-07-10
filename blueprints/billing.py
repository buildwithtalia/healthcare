from flask import jsonify, request
from datetime import datetime, timezone

from api_helpers import make_crud_blueprint
from services import (
    ServiceError, patients_svc, claims_svc, invoices_svc,
    notifications_svc, require,
)
import data_store as ds


def _validate_invoice(payload):
    require(patients_svc, payload.get("patient_id"), "patient")
    if payload.get("claim_id") is not None:
        require(claims_svc, payload.get("claim_id"), "claim")


invoices_bp = make_crud_blueprint(
    "invoices",
    "/api/invoices",
    ds.invoices,
    kind="invoice",
    required_fields=["patient_id", "total"],
    defaults={"status": "outstanding", "line_items": []},
    before_create=_validate_invoice,
)


@invoices_bp.get("/patient/<int:patient_id>")
def invoices_by_patient(patient_id):
    records = [r for r in ds.invoices.values() if r["patient_id"] == patient_id]
    return jsonify({"count": len(records), "items": records})


def _validate_payment(payload):
    invoice = require(invoices_svc, payload.get("invoice_id"), "invoice")
    payload.setdefault("patient_id", invoice["patient_id"])


payments_bp = make_crud_blueprint(
    "payments",
    "/api/payments",
    ds.payments,
    kind="payment",
    required_fields=["invoice_id", "amount"],
    defaults={"status": "pending", "method": "card"},
    before_create=_validate_payment,
)


@payments_bp.post("/pay")
def pay():
    payload = request.get_json(silent=True) or {}
    invoice_id = payload.get("invoice_id")
    amount = payload.get("amount")
    if invoice_id is None or amount is None:
        return jsonify({"error": "invoice_id and amount required"}), 400
    try:
        invoice = invoices_svc.get(f"/{invoice_id}")
    except ServiceError as e:
        body, code = e.to_response()
        return jsonify(body), code
    try:
        amount = float(amount)
    except (TypeError, ValueError):
        return jsonify({"error": "amount must be a number"}), 400

    new_balance = max(0.0, float(invoice.get("balance", invoice["total"])) - amount)
    status = "paid" if new_balance == 0 else invoice.get("status", "outstanding")
    try:
        invoice = invoices_svc.patch(
            f"/{invoice_id}", json={"balance": new_balance, "status": status}
        )
    except ServiceError as e:
        body, code = e.to_response()
        return jsonify(body), code

    from data_store import next_id
    payment = {
        "id": next_id("payment"),
        "invoice_id": invoice_id,
        "patient_id": invoice["patient_id"],
        "amount": amount,
        "method": payload.get("method", "card"),
        "paid_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "status": "posted",
    }
    ds.payments[payment["id"]] = payment
    try:
        notifications_svc.post("/send", json={
            "patient_id": invoice["patient_id"],
            "channel": "email",
            "subject": "Payment received",
            "message": f"Thank you. We received ${amount:.2f}. New balance: ${new_balance:.2f}.",
        })
    except ServiceError:
        pass
    return jsonify({"payment": payment, "invoice": invoice}), 201
