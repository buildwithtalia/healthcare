from flask import jsonify, request

from api_helpers import make_crud_blueprint
from services import (
    ServiceError, patients_svc, providers_svc, notifications_svc, require,
)
import data_store as ds


def _validate(payload):
    require(patients_svc, payload.get("patient_id"), "patient")
    if payload.get("prescriber_id") is not None:
        require(providers_svc, payload.get("prescriber_id"), "provider")


bp = make_crud_blueprint(
    "pharmacy",
    "/api/pharmacy",
    ds.prescriptions,
    kind="rx",
    required_fields=["patient_id", "drug", "dose"],
    defaults={"status": "active", "refills": 0},
    before_create=_validate,
)


@bp.get("/patient/<int:patient_id>")
def by_patient(patient_id):
    records = [r for r in ds.prescriptions.values() if r["patient_id"] == patient_id]
    return jsonify({"count": len(records), "items": records})


@bp.post("/<int:rx_id>/refill")
def refill(rx_id):
    rx = ds.prescriptions.get(rx_id)
    if not rx:
        return jsonify({"error": "prescription not found"}), 404
    if rx.get("refills", 0) <= 0:
        return jsonify({"error": "no refills remaining"}), 400
    rx["refills"] -= 1
    rx["last_refill_requested"] = request.get_json(silent=True) or {}
    try:
        notifications_svc.post("/send", json={
            "patient_id": rx["patient_id"],
            "channel": "sms",
            "subject": "Refill submitted",
            "message": f"Refill requested for {rx.get('drug')} {rx.get('dose', '')}.",
        })
    except ServiceError:
        pass
    return jsonify(rx)
