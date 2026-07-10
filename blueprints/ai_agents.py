from flask import jsonify, request

from api_helpers import make_crud_blueprint
from services import (
    ServiceError, patients_svc, ehr_svc, lab_svc, pharmacy_svc, appointments_svc,
)
import data_store as ds

bp = make_crud_blueprint(
    "ai_agents",
    "/api/ai-agents",
    ds.ai_agents,
    kind="agent",
    required_fields=["name", "version", "purpose"],
    defaults={"status": "staging", "capabilities": []},
)


@bp.post("/<int:agent_id>/deploy")
def deploy(agent_id):
    agent = ds.ai_agents.get(agent_id)
    if not agent:
        return jsonify({"error": "agent not found"}), 404
    agent["status"] = "deployed"
    return jsonify(agent)


@bp.post("/<int:agent_id>/retire")
def retire(agent_id):
    agent = ds.ai_agents.get(agent_id)
    if not agent:
        return jsonify({"error": "agent not found"}), 404
    agent["status"] = "retired"
    return jsonify(agent)


@bp.post("/<int:agent_id>/invoke")
def invoke(agent_id):
    """Invoke an agent. Some agents pull real clinical context from other APIs."""
    agent = ds.ai_agents.get(agent_id)
    if not agent:
        return jsonify({"error": "agent not found"}), 404
    if agent.get("status") != "deployed":
        return jsonify({"error": f"agent is {agent.get('status')}, not deployed"}), 409

    payload = request.get_json(silent=True) or {}
    patient_id = payload.get("patient_id")
    context = {}
    calls = []

    if patient_id is not None:
        try:
            context["patient"] = patients_svc.get(f"/{patient_id}")
            calls.append("patients")
        except ServiceError as e:
            body, code = e.to_response()
            return jsonify(body), code

        # Triage-style agent pulls EHR + labs + rx to draft its reply.
        name = (agent.get("name") or "").lower()
        try:
            if "triage" in name or "reader" in name:
                context["ehr"] = ehr_svc.get(f"/patient/{patient_id}")["items"]
                context["labs"] = lab_svc.get(f"/patient/{patient_id}")["items"]
                calls.extend(["ehr", "lab"])
            if "refill" in name:
                context["prescriptions"] = pharmacy_svc.get(f"/patient/{patient_id}")["items"]
                calls.append("pharmacy")
            if "triage" in name:
                context["upcoming_appointments"] = [
                    a for a in appointments_svc.get("/")["items"]
                    if a.get("patient_id") == patient_id
                ]
                calls.append("appointments")
        except ServiceError as e:
            body, code = e.to_response()
            return jsonify(body), code

    return jsonify({
        "agent_id": agent_id,
        "agent_name": agent["name"],
        "input": payload,
        "context_sources": calls,
        "context_summary": {k: (len(v) if isinstance(v, list) else "1 record") for k, v in context.items()},
        "output": {
            "reply": f"[{agent['name']}] processed request using {len(calls)} upstream services",
            "confidence": 0.87,
        },
    })
