# Healthcare Platform

A Flask application demonstrating twelve core healthcare service APIs with a
browsable dashboard, in-memory data store, and seed data.

## Run

```bash
pip install -r requirements.txt
python app.py
```

Then open http://127.0.0.1:5000.

## Services

| API           | Base path             | Purpose                                    |
| ------------- | --------------------- | ------------------------------------------ |
| Patients      | `/api/patients`       | Demographics, identifiers, contacts        |
| Appointments  | `/api/appointments`   | Scheduling and calendars                   |
| Providers     | `/api/providers`      | Physicians, nurses, specialists            |
| EHR           | `/api/ehr`            | Clinical records                           |
| Lab           | `/api/lab`            | Bloodwork and test results                 |
| Imaging       | `/api/imaging`        | X-rays, CT, MRI                            |
| Pharmacy      | `/api/pharmacy`       | Prescriptions                              |
| Insurance     | `/api/insurance`      | Eligibility and coverage                   |
| Claims        | `/api/claims`         | Adjudicated claims                         |
| Invoices      | `/api/invoices`       | Patient invoices                           |
| Payments      | `/api/payments`       | Payment posting                            |
| Notifications | `/api/notifications`  | Email/SMS/push                             |
| Devices       | `/api/devices`        | Wearables and remote monitoring            |
| AI Agents     | `/api/ai-agents`      | Registry of deployed agents                |

Every service supports standard REST:

- `GET    <base>/`         — list (with `?limit`, `?offset`, `?field=value`)
- `POST   <base>/`         — create
- `GET    <base>/<id>`     — read
- `PUT|PATCH <base>/<id>`  — update
- `DELETE <base>/<id>`     — remove

## Notable endpoints

- `GET /api/health` — service counts
- `GET /api/catalog` — machine-readable service catalog
- `GET /api/patients/<id>/summary` — patient plus all linked records
- `GET /api/patients/search?q=<term>`
- `GET /api/providers/<id>/schedule`
- `POST /api/appointments/<id>/cancel`
- `POST /api/appointments/<id>/check-in`
- `GET /api/lab/abnormal`
- `POST /api/pharmacy/<id>/refill`
- `GET /api/insurance/<id>/eligibility`
- `POST /api/claims/<id>/adjudicate`
- `POST /api/payments/pay`
- `POST /api/notifications/send`
- `GET|POST /api/devices/<id>/readings`
- `POST /api/ai-agents/<id>/deploy | /retire | /invoke`

## Example

```bash
# List patients
curl http://127.0.0.1:5000/api/patients/

# Create a patient
curl -X POST http://127.0.0.1:5000/api/patients/ \
  -H "Content-Type: application/json" \
  -d '{"first_name":"Sam","last_name":"Ito","dob":"1990-01-15"}'

# Pay an invoice
curl -X POST http://127.0.0.1:5000/api/payments/pay \
  -H "Content-Type: application/json" \
  -d '{"invoice_id": 1013, "amount": 45.0, "method": "card"}'
```

Data lives in-memory (see `data_store.py`) and reseeds every process start.
