"""MongoDB-backed data store for the healthcare platform.

Each module-level name (patients, providers, …) is a MongoCollection
proxy that supports the same dict-like read patterns used throughout
the blueprints (.get, .values, .keys, iteration) as well as direct
PyMongo operations.

The seed() function is idempotent: it only inserts data when the
database is empty, so restarting the server never duplicates records.
"""
from datetime import datetime, timedelta
from threading import Lock

from db import get_db


# ---------------------------------------------------------------------------
# Numeric ID counter (stored in MongoDB so it survives restarts)
# ---------------------------------------------------------------------------

_id_locks: dict[str, Lock] = {}


def next_id(kind: str) -> int:
    """Return the next auto-increment integer id for *kind*.

    Uses a MongoDB 'counters' collection with findOneAndUpdate so the
    sequence is safe under concurrent requests.
    """
    if kind not in _id_locks:
        _id_locks[kind] = Lock()
    with _id_locks[kind]:
        db = get_db()
        result = db.counters.find_one_and_update(
            {"_id": kind},
            {"$inc": {"seq": 1}},
            upsert=True,
            return_document=True,  # pymongo ReturnDocument.AFTER equivalent
        )
        return result["seq"]


def iso(dt: datetime) -> str:
    return dt.replace(microsecond=0).isoformat() + "Z"


NOW = datetime(2026, 7, 10, 9, 0, 0)


# ---------------------------------------------------------------------------
# MongoCollection proxy
# ---------------------------------------------------------------------------

class MongoCollection:
    """Thin wrapper around a pymongo Collection.

    Provides the dict-like interface (get, values, keys, __contains__,
    __len__, __iter__, __getitem__, __setitem__, __delitem__) that the
    existing blueprints and api_helpers rely on, while delegating all
    persistence to MongoDB.

    Records are stored with a numeric 'id' field (not _id).  The
    MongoDB _id is set equal to the numeric id for easy look-ups.
    """

    def __init__(self, collection_name: str):
        self._name = collection_name

    @property
    def _col(self):
        return get_db()[self._name]

    # ------------------------------------------------------------------
    # dict-like helpers
    # ------------------------------------------------------------------

    def get(self, key, default=None):
        doc = self._col.find_one({"id": key}, {"_id": 0})
        return doc if doc is not None else default

    def values(self):
        return list(self._col.find({}, {"_id": 0}))

    def keys(self):
        return [d["id"] for d in self._col.find({}, {"id": 1, "_id": 0})]

    def items(self):
        docs = self._col.find({}, {"_id": 0})
        return [(d["id"], d) for d in docs]

    def __contains__(self, key):
        return self._col.count_documents({"id": key}, limit=1) > 0

    def __len__(self):
        return self._col.count_documents({})

    def __iter__(self):
        return iter(self.keys())

    def __getitem__(self, key):
        doc = self.get(key)
        if doc is None:
            raise KeyError(key)
        return doc

    def __setitem__(self, key, value):
        value["id"] = key
        self._col.replace_one({"id": key}, {**value, "_id": key}, upsert=True)

    def __delitem__(self, key):
        result = self._col.delete_one({"id": key})
        if result.deleted_count == 0:
            raise KeyError(key)


# ---------------------------------------------------------------------------
# Module-level collection objects (same names as before)
# ---------------------------------------------------------------------------

patients          = MongoCollection("patients")
providers         = MongoCollection("providers")
appointments      = MongoCollection("appointments")
ehr_records       = MongoCollection("ehr_records")
lab_results       = MongoCollection("lab_results")
imaging_studies   = MongoCollection("imaging_studies")
prescriptions     = MongoCollection("prescriptions")
insurance_policies = MongoCollection("insurance_policies")
claims            = MongoCollection("claims")
invoices          = MongoCollection("invoices")
payments          = MongoCollection("payments")
notifications     = MongoCollection("notifications")
devices           = MongoCollection("devices")
device_readings   = MongoCollection("device_readings")
ai_agents         = MongoCollection("ai_agents")


def _add(store: MongoCollection, kind: str, record: dict) -> dict:
    rid = next_id(kind)
    record["id"] = rid
    store[rid] = record
    return record


def seed():
    # Only seed when the database is empty to keep the function idempotent.
    if len(patients) > 0:
        return

    _add(patients, "patient", {
        "mrn": "MRN-001",
        "first_name": "Ava",
        "last_name": "Reyes",
        "dob": "1988-03-14",
        "gender": "female",
        "email": "ava.reyes@example.com",
        "phone": "+1-555-0110",
        "address": "42 Maple Ave, Boston, MA",
        "blood_type": "O+",
        "allergies": ["penicillin"],
        "created_at": iso(NOW - timedelta(days=900)),
    })
    _add(patients, "patient", {
        "mrn": "MRN-002",
        "first_name": "Julian",
        "last_name": "Okafor",
        "dob": "1975-11-02",
        "gender": "male",
        "email": "julian.okafor@example.com",
        "phone": "+1-555-0111",
        "address": "108 Cedar St, Cambridge, MA",
        "blood_type": "A-",
        "allergies": [],
        "created_at": iso(NOW - timedelta(days=730)),
    })
    _add(patients, "patient", {
        "mrn": "MRN-003",
        "first_name": "Priya",
        "last_name": "Shah",
        "dob": "1992-06-21",
        "gender": "female",
        "email": "priya.shah@example.com",
        "phone": "+1-555-0112",
        "address": "9 Beacon Rd, Somerville, MA",
        "blood_type": "B+",
        "allergies": ["sulfa", "latex"],
        "created_at": iso(NOW - timedelta(days=500)),
    })

    _add(providers, "provider", {
        "npi": "1122334455",
        "first_name": "Elena",
        "last_name": "Marsh",
        "specialty": "Cardiology",
        "role": "physician",
        "email": "e.marsh@clinic.example",
        "phone": "+1-555-0201",
        "department": "Cardiology",
        "active": True,
    })
    _add(providers, "provider", {
        "npi": "2233445566",
        "first_name": "Marcus",
        "last_name": "Chen",
        "specialty": "Family Medicine",
        "role": "physician",
        "email": "m.chen@clinic.example",
        "phone": "+1-555-0202",
        "department": "Primary Care",
        "active": True,
    })
    _add(providers, "provider", {
        "npi": "3344556677",
        "first_name": "Nadia",
        "last_name": "Alvarez",
        "specialty": "Nursing",
        "role": "nurse",
        "email": "n.alvarez@clinic.example",
        "phone": "+1-555-0203",
        "department": "Primary Care",
        "active": True,
    })

    pids = list(patients.keys())
    prids = list(providers.keys())

    _add(appointments, "appointment", {
        "patient_id": pids[0],
        "provider_id": prids[0],
        "start_time": iso(NOW + timedelta(days=1, hours=1)),
        "end_time": iso(NOW + timedelta(days=1, hours=1, minutes=30)),
        "reason": "Annual cardiac follow-up",
        "location": "Suite 3B",
        "status": "scheduled",
    })
    _add(appointments, "appointment", {
        "patient_id": pids[1],
        "provider_id": prids[1],
        "start_time": iso(NOW + timedelta(days=2, hours=3)),
        "end_time": iso(NOW + timedelta(days=2, hours=3, minutes=20)),
        "reason": "Blood pressure check",
        "location": "Suite 1A",
        "status": "scheduled",
    })
    _add(appointments, "appointment", {
        "patient_id": pids[2],
        "provider_id": prids[1],
        "start_time": iso(NOW - timedelta(days=5)),
        "end_time": iso(NOW - timedelta(days=5, hours=-1)),
        "reason": "Cough and fever",
        "location": "Suite 1A",
        "status": "completed",
    })

    _add(ehr_records, "ehr", {
        "patient_id": pids[0],
        "provider_id": prids[0],
        "visit_date": iso(NOW - timedelta(days=90)),
        "chief_complaint": "Palpitations",
        "diagnosis": ["I49.9 - Cardiac arrhythmia, unspecified"],
        "notes": "Holter monitor ordered. Continue metoprolol 25mg BID.",
        "vitals": {"bp": "128/82", "hr": 78, "temp_c": 36.8, "spo2": 98},
    })
    _add(ehr_records, "ehr", {
        "patient_id": pids[2],
        "provider_id": prids[1],
        "visit_date": iso(NOW - timedelta(days=5)),
        "chief_complaint": "Cough and fever",
        "diagnosis": ["J06.9 - Acute upper respiratory infection"],
        "notes": "Symptomatic care. Rest and fluids.",
        "vitals": {"bp": "118/74", "hr": 88, "temp_c": 38.1, "spo2": 97},
    })

    _add(lab_results, "lab", {
        "patient_id": pids[0],
        "ordered_by": prids[0],
        "panel": "Lipid Panel",
        "collected_at": iso(NOW - timedelta(days=88)),
        "results": [
            {"analyte": "Total Cholesterol", "value": 212, "unit": "mg/dL", "flag": "H"},
            {"analyte": "LDL", "value": 138, "unit": "mg/dL", "flag": "H"},
            {"analyte": "HDL", "value": 52, "unit": "mg/dL", "flag": "N"},
            {"analyte": "Triglycerides", "value": 160, "unit": "mg/dL", "flag": "N"},
        ],
        "status": "final",
    })
    _add(lab_results, "lab", {
        "patient_id": pids[2],
        "ordered_by": prids[1],
        "panel": "CBC",
        "collected_at": iso(NOW - timedelta(days=5)),
        "results": [
            {"analyte": "WBC", "value": 11.2, "unit": "10^3/uL", "flag": "H"},
            {"analyte": "RBC", "value": 4.6, "unit": "10^6/uL", "flag": "N"},
            {"analyte": "Hgb", "value": 13.8, "unit": "g/dL", "flag": "N"},
        ],
        "status": "final",
    })

    _add(imaging_studies, "imaging", {
        "patient_id": pids[0],
        "ordered_by": prids[0],
        "modality": "MRI",
        "body_part": "Cardiac",
        "study_date": iso(NOW - timedelta(days=60)),
        "findings": "Normal LV function. Mild mitral regurgitation.",
        "impression": "No acute abnormality.",
        "status": "final",
        "image_url": "https://example.hospital/imaging/9001.dcm",
    })
    _add(imaging_studies, "imaging", {
        "patient_id": pids[1],
        "ordered_by": prids[1],
        "modality": "X-ray",
        "body_part": "Chest",
        "study_date": iso(NOW - timedelta(days=180)),
        "findings": "Clear lung fields.",
        "impression": "No acute cardiopulmonary process.",
        "status": "final",
        "image_url": "https://example.hospital/imaging/9002.dcm",
    })

    _add(prescriptions, "rx", {
        "patient_id": pids[0],
        "prescriber_id": prids[0],
        "drug": "Metoprolol",
        "dose": "25 mg",
        "route": "PO",
        "frequency": "BID",
        "quantity": 60,
        "refills": 3,
        "written_at": iso(NOW - timedelta(days=90)),
        "status": "active",
    })
    _add(prescriptions, "rx", {
        "patient_id": pids[2],
        "prescriber_id": prids[1],
        "drug": "Amoxicillin",
        "dose": "500 mg",
        "route": "PO",
        "frequency": "TID",
        "quantity": 21,
        "refills": 0,
        "written_at": iso(NOW - timedelta(days=5)),
        "status": "active",
    })

    _add(insurance_policies, "insurance", {
        "patient_id": pids[0],
        "carrier": "BlueShield National",
        "plan": "PPO Gold",
        "member_id": "BSN-88213",
        "group_id": "GRP-4421",
        "effective_date": "2026-01-01",
        "termination_date": None,
        "copay": 25,
        "deductible": 1500,
        "status": "active",
    })
    _add(insurance_policies, "insurance", {
        "patient_id": pids[1],
        "carrier": "Aetna",
        "plan": "HMO Silver",
        "member_id": "AET-55901",
        "group_id": "GRP-7702",
        "effective_date": "2025-07-01",
        "termination_date": None,
        "copay": 35,
        "deductible": 2500,
        "status": "active",
    })

    ins_id = list(insurance_policies.keys())[0]
    _add(claims, "claim", {
        "patient_id": pids[0],
        "insurance_id": ins_id,
        "provider_id": prids[0],
        "service_date": iso(NOW - timedelta(days=90)),
        "cpt_codes": ["99214", "93000"],
        "amount_billed": 480.0,
        "amount_allowed": 320.0,
        "status": "paid",
        "submitted_at": iso(NOW - timedelta(days=85)),
    })

    _add(invoices, "invoice", {
        "patient_id": pids[0],
        "claim_id": list(claims.keys())[0],
        "issued_at": iso(NOW - timedelta(days=30)),
        "due_date": (NOW + timedelta(days=15)).strftime("%Y-%m-%d"),
        "line_items": [
            {"desc": "Office visit level 4", "amount": 25.0},
            {"desc": "EKG (patient responsibility)", "amount": 20.0},
        ],
        "total": 45.0,
        "balance": 45.0,
        "status": "outstanding",
    })

    _add(payments, "payment", {
        "invoice_id": list(invoices.keys())[0],
        "patient_id": pids[0],
        "amount": 0.0,
        "method": "none",
        "paid_at": None,
        "status": "pending",
    })

    _add(notifications, "notification", {
        "patient_id": pids[0],
        "channel": "email",
        "subject": "Appointment reminder",
        "message": "You have a cardiology visit tomorrow at 10:00 AM.",
        "sent_at": iso(NOW - timedelta(hours=6)),
        "status": "sent",
    })
    _add(notifications, "notification", {
        "patient_id": pids[1],
        "channel": "sms",
        "subject": "Refill ready",
        "message": "Your prescription is ready for pickup.",
        "sent_at": iso(NOW - timedelta(hours=24)),
        "status": "sent",
    })

    dev1 = _add(devices, "device", {
        "patient_id": pids[0],
        "type": "wearable",
        "model": "CardioBand X2",
        "serial": "CBX2-000123",
        "registered_at": iso(NOW - timedelta(days=200)),
        "status": "active",
    })
    dev2 = _add(devices, "device", {
        "patient_id": pids[2],
        "type": "glucometer",
        "model": "GlucoTrack G7",
        "serial": "GT7-991002",
        "registered_at": iso(NOW - timedelta(days=45)),
        "status": "active",
    })

    _add(device_readings, "reading", {
        "device_id": dev1["id"],
        "patient_id": pids[0],
        "metric": "heart_rate",
        "value": 72,
        "unit": "bpm",
        "recorded_at": iso(NOW - timedelta(minutes=15)),
    })
    _add(device_readings, "reading", {
        "device_id": dev2["id"],
        "patient_id": pids[2],
        "metric": "glucose",
        "value": 118,
        "unit": "mg/dL",
        "recorded_at": iso(NOW - timedelta(hours=2)),
    })

    _add(ai_agents, "agent", {
        "name": "Triage Assistant",
        "version": "1.4.0",
        "purpose": "Front-desk symptom triage and appointment recommendation",
        "owner": "AI Platform",
        "endpoint": "https://agents.hospital.example/triage",
        "capabilities": ["symptom_check", "appointment_booking"],
        "status": "deployed",
        "created_at": iso(NOW - timedelta(days=120)),
    })
    _add(ai_agents, "agent", {
        "name": "Radiology Reader",
        "version": "2.0.1",
        "purpose": "Assists radiologists with X-ray anomaly detection",
        "owner": "Radiology Informatics",
        "endpoint": "https://agents.hospital.example/rad-reader",
        "capabilities": ["image_classification", "report_drafting"],
        "status": "deployed",
        "created_at": iso(NOW - timedelta(days=60)),
    })
    _add(ai_agents, "agent", {
        "name": "Refill Bot",
        "version": "0.9.0",
        "purpose": "Handles prescription refill requests via SMS",
        "owner": "Pharmacy",
        "endpoint": "https://agents.hospital.example/refill",
        "capabilities": ["intent_classification", "workflow_orchestration"],
        "status": "staging",
        "created_at": iso(NOW - timedelta(days=14)),
    })


seed()
