from flask import jsonify

from api_helpers import make_crud_blueprint
from services import (
    ServiceError, patients_svc, providers_svc, notifications_svc, require,
)
import data_store as ds


def _validate(payload):
    require(patients_svc, payload.get("patient_id"), "patient")
    if payload.get("ordered_by") is not None:
        require(providers_svc, payload.get("ordered_by"), "provider")


def _notify_if_abnormal(record):
    if not any(r.get("flag") in ("H", "L", "A") for r in record.get("results", [])):
        return
    try:
        notifications_svc.post("/send", json={
            "patient_id": record["patient_id"],
            "channel": "email",
            "subject": "Lab results available",
            "message": f"Your {record.get('panel', 'lab')} results include abnormal values. Your provider will contact you.",
        })
    except ServiceError:
        pass


bp = make_crud_blueprint(
    "lab",
    "/api/lab",
    ds.lab_results,
    kind="lab",
    required_fields=["patient_id", "panel"],
    defaults={"results": [], "status": "ordered"},
    before_create=_validate,
    after_create=_notify_if_abnormal,
)


@bp.get("/patient/<int:patient_id>")
def by_patient(patient_id):
    records = [r for r in ds.lab_results.values() if r["patient_id"] == patient_id]
    return jsonify({"count": len(records), "items": records})


@bp.get("/abnormal")
def abnormal():
    abnormal = []
    for r in ds.lab_results.values():
        if any(res.get("flag") in ("H", "L", "A") for res in r.get("results", [])):
            abnormal.append(r)
    return jsonify({"count": len(abnormal), "items": abnormal})
