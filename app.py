"""Healthcare Platform - Flask application entry point.

Registers all API blueprints, exposes a browsable dashboard, and includes
a machine-readable service catalog at /api/catalog.
"""
from flask import Flask, jsonify, render_template
from flask_cors import CORS

import data_store as ds
from db import get_db
from blueprints.patients import bp as patients_bp
from blueprints.providers import bp as providers_bp
from blueprints.appointments import bp as appointments_bp
from blueprints.ehr import bp as ehr_bp
from blueprints.lab import bp as lab_bp
from blueprints.imaging import bp as imaging_bp
from blueprints.pharmacy import bp as pharmacy_bp
from blueprints.insurance import bp as insurance_bp, claims_bp
from blueprints.billing import invoices_bp, payments_bp
from blueprints.notifications import bp as notifications_bp
from blueprints.devices import bp as devices_bp
from blueprints.ai_agents import bp as ai_agents_bp


def create_app():
    app = Flask(__name__)
    CORS(app)

    for bp in (
        patients_bp,
        providers_bp,
        appointments_bp,
        ehr_bp,
        lab_bp,
        imaging_bp,
        pharmacy_bp,
        insurance_bp,
        claims_bp,
        invoices_bp,
        payments_bp,
        notifications_bp,
        devices_bp,
        ai_agents_bp,
    ):
        app.register_blueprint(bp)

    @app.get("/")
    def index():
        return render_template("index.html", services=SERVICE_CATALOG)

    @app.get("/api")
    def api_root():
        return jsonify({
            "name": "Healthcare Platform API",
            "version": "1.0.0",
            "services": [s["slug"] for s in SERVICE_CATALOG],
        })

    @app.get("/api/catalog")
    def catalog():
        return jsonify(SERVICE_CATALOG)

    @app.get("/api/health")
    def health():
        # Verify MongoDB connectivity with a lightweight ping
        try:
            get_db().command("ping")
            db_status = "ok"
        except Exception as exc:
            db_status = f"error: {exc}"

        return jsonify({
            "status": "ok" if db_status == "ok" else "degraded",
            "database": db_status,
            "counts": {
                "patients": len(ds.patients),
                "providers": len(ds.providers),
                "appointments": len(ds.appointments),
                "ehr": len(ds.ehr_records),
                "lab": len(ds.lab_results),
                "imaging": len(ds.imaging_studies),
                "prescriptions": len(ds.prescriptions),
                "insurance": len(ds.insurance_policies),
                "claims": len(ds.claims),
                "invoices": len(ds.invoices),
                "payments": len(ds.payments),
                "notifications": len(ds.notifications),
                "devices": len(ds.devices),
                "device_readings": len(ds.device_readings),
                "ai_agents": len(ds.ai_agents),
            },
        })

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "not found"}), 404

    return app


SERVICE_CATALOG = [
    {"slug": "patients",      "name": "Patient API",       "base": "/api/patients",      "description": "Demographics, identifiers, contacts",
     "depends_on": []},
    {"slug": "appointments",  "name": "Appointment API",   "base": "/api/appointments",  "description": "Scheduling and calendars",
     "depends_on": ["patients", "providers", "notifications"]},
    {"slug": "providers",     "name": "Provider API",      "base": "/api/providers",     "description": "Physicians, nurses, specialists",
     "depends_on": []},
    {"slug": "ehr",           "name": "EHR API",           "base": "/api/ehr",           "description": "Clinical records",
     "depends_on": ["patients", "providers"]},
    {"slug": "lab",           "name": "Lab API",           "base": "/api/lab",           "description": "Bloodwork and test results",
     "depends_on": ["patients", "providers", "notifications"]},
    {"slug": "imaging",       "name": "Imaging API",       "base": "/api/imaging",       "description": "X-rays, CT, MRI",
     "depends_on": ["patients", "providers"]},
    {"slug": "pharmacy",      "name": "Pharmacy API",      "base": "/api/pharmacy",      "description": "Prescriptions",
     "depends_on": ["patients", "providers", "notifications"]},
    {"slug": "insurance",     "name": "Insurance API",     "base": "/api/insurance",     "description": "Eligibility and claims",
     "depends_on": ["patients"]},
    {"slug": "claims",        "name": "Claims API",        "base": "/api/claims",        "description": "Insurance claim submissions",
     "depends_on": ["patients", "providers", "insurance"]},
    {"slug": "invoices",      "name": "Invoice API",       "base": "/api/invoices",      "description": "Patient billing invoices",
     "depends_on": ["patients", "claims"]},
    {"slug": "payments",      "name": "Payment API",       "base": "/api/payments",      "description": "Payment posting",
     "depends_on": ["invoices", "notifications"]},
    {"slug": "notifications", "name": "Notification API",  "base": "/api/notifications", "description": "Email/SMS/push",
     "depends_on": ["patients"]},
    {"slug": "devices",       "name": "Device API",        "base": "/api/devices",       "description": "Wearables and remote monitoring",
     "depends_on": ["patients", "notifications"]},
    {"slug": "ai_agents",     "name": "AI Agent API",      "base": "/api/ai-agents",     "description": "Registry of deployed agents",
     "depends_on": ["patients", "ehr", "lab", "pharmacy", "appointments"]},
]


app = create_app()


if __name__ == "__main__":
    # threaded=True is required because APIs make HTTP calls to each other in-process.
    app.run(host="127.0.0.1", port=5000, debug=False, threaded=True)
