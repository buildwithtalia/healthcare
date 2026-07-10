from flask import jsonify, request

from api_helpers import make_crud_blueprint
from services import (
    ServiceError, patients_svc, providers_svc, insurance_svc, require,
)
import data_store as ds


def _validate_policy(payload):
    require(patients_svc, payload.get("patient_id"), "patient")


bp = make_crud_blueprint(
    "insurance",
    "/api/insurance",
    ds.insurance_policies,
    kind="insurance",
    required_fields=["patient_id", "carrier", "member_id"],
    defaults={"status": "active"},
    before_create=_validate_policy,
)


@bp.get("/patient/<int:patient_id>")
def by_patient(patient_id):
    records = [r for r in ds.insurance_policies.values() if r["patient_id"] == patient_id]
    return jsonify({"count": len(records), "items": records})


@bp.get("/<int:policy_id>/eligibility")
def eligibility(policy_id):
    policy = ds.insurance_policies.get(policy_id)
    if not policy:
        return jsonify({"error": "policy not found"}), 404
    try:
        patient = patients_svc.get(f"/{policy['patient_id']}")
    except ServiceError as e:
        body, code = e.to_response()
        return jsonify(body), code
    eligible = policy.get("status") == "active"
    return jsonify({
        "policy_id": policy_id,
        "patient": {
            "id": patient["id"],
            "name": f"{patient.get('first_name','')} {patient.get('last_name','')}".strip(),
            "mrn": patient.get("mrn"),
        },
        "eligible": eligible,
        "copay": policy.get("copay"),
        "deductible": policy.get("deductible"),
        "carrier": policy.get("carrier"),
        "plan": policy.get("plan"),
    })


def _validate_claim(payload):
    require(patients_svc, payload.get("patient_id"), "patient")
    require(insurance_svc, payload.get("insurance_id"), "insurance")
    if payload.get("provider_id") is not None:
        require(providers_svc, payload.get("provider_id"), "provider")


claims_bp = make_crud_blueprint(
    "claims",
    "/api/claims",
    ds.claims,
    kind="claim",
    required_fields=["patient_id", "insurance_id", "amount_billed"],
    defaults={"status": "submitted"},
    before_create=_validate_claim,
)


@claims_bp.post("/<int:claim_id>/adjudicate")
def adjudicate(claim_id):
    claim = ds.claims.get(claim_id)
    if not claim:
        return jsonify({"error": "claim not found"}), 404
    payload = request.get_json(silent=True) or {}
    claim["status"] = payload.get("status", "adjudicated")
    claim["amount_allowed"] = payload.get("amount_allowed", claim.get("amount_allowed"))
    return jsonify(claim)
