from flask import jsonify, request
from datetime import datetime, timezone

from api_helpers import make_crud_blueprint
from services import (
    ServiceError, patients_svc, notifications_svc, require,
)
import data_store as ds


ABNORMAL_THRESHOLDS = {
    "heart_rate": lambda v: v < 40 or v > 120,
    "glucose": lambda v: v < 70 or v > 200,
    "spo2": lambda v: v < 92,
    "blood_pressure_systolic": lambda v: v > 160 or v < 90,
}


def _validate(payload):
    require(patients_svc, payload.get("patient_id"), "patient")


bp = make_crud_blueprint(
    "devices",
    "/api/devices",
    ds.devices,
    kind="device",
    required_fields=["patient_id", "type", "model"],
    defaults={"status": "active"},
    before_create=_validate,
)


@bp.get("/<int:device_id>/readings")
def readings(device_id):
    records = [r for r in ds.device_readings.values() if r["device_id"] == device_id]
    records.sort(key=lambda r: r.get("recorded_at", ""), reverse=True)
    return jsonify({"count": len(records), "items": records})


@bp.post("/<int:device_id>/readings")
def ingest_reading(device_id):
    device = ds.devices.get(device_id)
    if not device:
        return jsonify({"error": "device not found"}), 404
    payload = request.get_json(silent=True) or {}
    if "metric" not in payload or "value" not in payload:
        return jsonify({"error": "metric and value required"}), 400
    from data_store import next_id
    reading = {
        "id": next_id("reading"),
        "device_id": device_id,
        "patient_id": device["patient_id"],
        "metric": payload["metric"],
        "value": payload["value"],
        "unit": payload.get("unit"),
        "recorded_at": payload.get(
            "recorded_at",
            datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        ),
    }
    ds.device_readings[reading["id"]] = reading

    check = ABNORMAL_THRESHOLDS.get(payload["metric"])
    if check:
        try:
            if check(float(payload["value"])) is True:
                notifications_svc.post("/send", json={
                    "patient_id": device["patient_id"],
                    "channel": "push",
                    "subject": f"Abnormal {payload['metric']} reading",
                    "message": f"Reading {payload['value']} {payload.get('unit','')} is outside normal range.",
                })
                reading["alerted"] = True
        except (ServiceError, ValueError, TypeError):
            pass
    return jsonify(reading), 201
