from flask import Blueprint, jsonify, request
from api_helpers import make_crud_blueprint
import data_store as ds

bp = make_crud_blueprint(
    "patients",
    "/api/patients",
    ds.patients,
    kind="patient",
    required_fields=["first_name", "last_name", "dob"],
    defaults={"allergies": [], "status": "active"},
)


@bp.get("/<int:patient_id>/summary")
def patient_summary(patient_id):
    patient = ds.patients.get(patient_id)
    if not patient:
        return jsonify({"error": "patient not found"}), 404
    return jsonify({
        "patient": patient,
        "appointments": [a for a in ds.appointments.values() if a["patient_id"] == patient_id],
        "ehr": [e for e in ds.ehr_records.values() if e["patient_id"] == patient_id],
        "labs": [l for l in ds.lab_results.values() if l["patient_id"] == patient_id],
        "imaging": [i for i in ds.imaging_studies.values() if i["patient_id"] == patient_id],
        "prescriptions": [p for p in ds.prescriptions.values() if p["patient_id"] == patient_id],
        "insurance": [ins for ins in ds.insurance_policies.values() if ins["patient_id"] == patient_id],
        "devices": [d for d in ds.devices.values() if d["patient_id"] == patient_id],
    })


@bp.get("/search")
def search():
    q = (request.args.get("q") or "").lower()
    if not q:
        return jsonify({"count": 0, "items": []})
    matches = []
    for p in ds.patients.values():
        haystack = " ".join([
            p.get("first_name", ""), p.get("last_name", ""),
            p.get("mrn", ""), p.get("email", ""), p.get("phone", ""),
        ]).lower()
        if q in haystack:
            matches.append(p)
    return jsonify({"count": len(matches), "items": matches})
