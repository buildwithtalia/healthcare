from flask import jsonify

from api_helpers import make_crud_blueprint
from services import patients_svc, providers_svc, require
import data_store as ds


def _validate(payload):
    require(patients_svc, payload.get("patient_id"), "patient")
    if payload.get("ordered_by") is not None:
        require(providers_svc, payload.get("ordered_by"), "provider")


bp = make_crud_blueprint(
    "imaging",
    "/api/imaging",
    ds.imaging_studies,
    kind="imaging",
    required_fields=["patient_id", "modality", "body_part"],
    defaults={"status": "scheduled"},
    before_create=_validate,
)


@bp.get("/patient/<int:patient_id>")
def by_patient(patient_id):
    records = [r for r in ds.imaging_studies.values() if r["patient_id"] == patient_id]
    return jsonify({"count": len(records), "items": records})
