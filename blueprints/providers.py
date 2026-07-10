from flask import jsonify, request
from api_helpers import make_crud_blueprint
import data_store as ds

bp = make_crud_blueprint(
    "providers",
    "/api/providers",
    ds.providers,
    kind="provider",
    required_fields=["first_name", "last_name", "role"],
    defaults={"active": True},
)


@bp.get("/<int:provider_id>/schedule")
def schedule(provider_id):
    if provider_id not in ds.providers:
        return jsonify({"error": "provider not found"}), 404
    appts = [a for a in ds.appointments.values() if a["provider_id"] == provider_id]
    return jsonify({"provider_id": provider_id, "appointments": appts})
