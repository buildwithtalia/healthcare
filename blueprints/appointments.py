from flask import jsonify, request

from api_helpers import make_crud_blueprint
from services import ServiceError, patients_svc, providers_svc, notifications_svc, require
import data_store as ds


def _validate_refs(payload):
    require(patients_svc, payload.get("patient_id"), "patient")
    require(providers_svc, payload.get("provider_id"), "provider")


bp = make_crud_blueprint(
    "appointments",
    "/api/appointments",
    ds.appointments,
    kind="appointment",
    required_fields=["patient_id", "provider_id", "start_time"],
    defaults={"status": "scheduled"},
    before_create=_validate_refs,
)


@bp.post("/<int:appt_id>/cancel")
def cancel(appt_id):
    appt = ds.appointments.get(appt_id)
    if not appt:
        return jsonify({"error": "appointment not found"}), 404
    appt["status"] = "cancelled"
    reason = (request.get_json(silent=True) or {}).get("reason")
    if reason:
        appt["cancellation_reason"] = reason
    try:
        notifications_svc.post("/send", json={
            "patient_id": appt["patient_id"],
            "channel": "email",
            "subject": "Appointment cancelled",
            "message": f"Your appointment on {appt.get('start_time')} was cancelled.",
        })
    except ServiceError:
        pass
    return jsonify(appt)


@bp.post("/<int:appt_id>/check-in")
def check_in(appt_id):
    appt = ds.appointments.get(appt_id)
    if not appt:
        return jsonify({"error": "appointment not found"}), 404
    appt["status"] = "checked-in"
    try:
        notifications_svc.post("/send", json={
            "patient_id": appt["patient_id"],
            "channel": "sms",
            "subject": "Checked in",
            "message": "You are checked in. A provider will be with you shortly.",
        })
    except ServiceError:
        pass
    return jsonify(appt)
