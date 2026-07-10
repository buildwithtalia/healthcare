from flask import jsonify, request
from datetime import datetime, timezone

from api_helpers import make_crud_blueprint
from services import ServiceError, patients_svc, require
import data_store as ds


def _validate(payload):
    require(patients_svc, payload.get("patient_id"), "patient")


bp = make_crud_blueprint(
    "notifications",
    "/api/notifications",
    ds.notifications,
    kind="notification",
    required_fields=["patient_id", "channel", "message"],
    defaults={"status": "queued"},
    before_create=_validate,
)


@bp.post("/send")
def send():
    """Look up the patient's contact via Patient API and 'send' a notification."""
    payload = request.get_json(silent=True) or {}
    for f in ("patient_id", "channel", "message"):
        if f not in payload:
            return jsonify({"error": f"missing: {f}"}), 400
    if payload["channel"] not in ("email", "sms", "push"):
        return jsonify({"error": "channel must be email|sms|push"}), 400
    try:
        patient = patients_svc.get(f"/{payload['patient_id']}")
    except ServiceError as e:
        body, code = e.to_response()
        return jsonify(body), code
    to = {
        "email": patient.get("email"),
        "sms": patient.get("phone"),
        "push": patient.get("mrn"),
    }[payload["channel"]]

    from data_store import next_id
    record = {
        "id": next_id("notification"),
        "patient_id": payload["patient_id"],
        "channel": payload["channel"],
        "subject": payload.get("subject", ""),
        "message": payload["message"],
        "to": to,
        "sent_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "status": "sent" if to else "failed",
    }
    ds.notifications[record["id"]] = record
    return jsonify(record), 201 if record["status"] == "sent" else 502
