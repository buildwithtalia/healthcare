"""Shared helpers for CRUD blueprints."""
from flask import Blueprint, jsonify, request, abort

from services import ServiceError


def make_crud_blueprint(
    name,
    url_prefix,
    store,
    kind,
    required_fields=None,
    defaults=None,
    before_create=None,
    after_create=None,
    before_update=None,
    after_update=None,
):
    """Build a Blueprint that exposes standard REST CRUD over a dict-based store.

    Hooks:
      before_create(payload)  -> may mutate payload; raise ServiceError to reject
      after_create(record)    -> side effects (e.g., notifications)
      before_update(existing, payload) -> may mutate; raise ServiceError to reject
      after_update(record)    -> side effects

    Routes:
      GET    /            list, supports ?field=value filters + limit/offset
      POST   /            create
      GET    /<id>        read
      PUT    /<id>        update
      PATCH  /<id>        partial update
      DELETE /<id>        remove
    """
    bp = Blueprint(name, __name__, url_prefix=url_prefix)
    required_fields = required_fields or []
    defaults = defaults or {}

    def apply_filters(records):
        for key, value in request.args.items():
            if key in ("limit", "offset"):
                continue
            records = [
                r for r in records
                if str(r.get(key, "")).lower() == value.lower()
            ]
        return records

    @bp.get("/")
    def list_records():
        items = apply_filters(list(store.values()))
        try:
            offset = int(request.args.get("offset", 0))
            limit = int(request.args.get("limit", 200))
        except ValueError:
            abort(400, "offset and limit must be integers")
        return jsonify({
            "count": len(items),
            "items": items[offset:offset + limit],
        })

    @bp.post("/")
    def create_record():
        from data_store import next_id
        payload = request.get_json(silent=True) or {}
        missing = [f for f in required_fields if f not in payload]
        if missing:
            return jsonify({"error": f"missing fields: {', '.join(missing)}"}), 400
        if before_create:
            try:
                before_create(payload)
            except ServiceError as e:
                body, code = e.to_response()
                return jsonify(body), code
        record = {**defaults, **payload}
        record["id"] = next_id(kind)
        store[record["id"]] = record
        if after_create:
            try:
                after_create(record)
            except ServiceError:
                # Side effects should not fail the primary write.
                pass
        return jsonify(record), 201

    @bp.get("/<int:record_id>")
    def read_record(record_id):
        record = store.get(record_id)
        if not record:
            return jsonify({"error": f"{kind} {record_id} not found"}), 404
        return jsonify(record)

    @bp.put("/<int:record_id>")
    @bp.patch("/<int:record_id>")
    def update_record(record_id):
        record = store.get(record_id)
        if not record:
            return jsonify({"error": f"{kind} {record_id} not found"}), 404
        payload = request.get_json(silent=True) or {}
        payload.pop("id", None)
        if before_update:
            try:
                before_update(record, payload)
            except ServiceError as e:
                body, code = e.to_response()
                return jsonify(body), code
        record.update(payload)
        store[record_id] = record
        if after_update:
            try:
                after_update(record)
            except ServiceError:
                pass
        return jsonify(record)

    @bp.delete("/<int:record_id>")
    def delete_record(record_id):
        if record_id not in store:
            return jsonify({"error": f"{kind} {record_id} not found"}), 404
        del store[record_id]
        return jsonify({"deleted": record_id})

    return bp
