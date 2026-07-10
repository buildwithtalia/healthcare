from flask import jsonify

from api_helpers import make_crud_blueprint
from services import patients_svc, providers_svc, require
import data_store as ds


def _validate(payload):
    require(patients_svc, payload.get("patient_id"), "patient")
    if payload.get("provider_id") is not None:
        require(providers_svc, payload.get("provider_id"), "provider")


bp = make_crud_blueprint(
    "ehr",
    "/api/ehr",
    ds.ehr_records,
    kind="ehr",
    required_fields=["patient_id", "visit_date"],
    defaults={"diagnosis": [], "notes": ""},
    before_create=_validate,
)


@bp.get("/patient/<int:patient_id>")
def by_patient(patient_id):
    records = [r for r in ds.ehr_records.values() if r["patient_id"] == patient_id]
    return jsonify({"count": len(records), "items": records})
