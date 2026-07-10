"""HTTP clients for inter-service calls.

Each API in this platform is a distinct service. Even though they run in the
same Flask process for demo purposes, they talk to each other over HTTP,
so the dependency graph is real: appointments cannot be created without a
successful Patient API + Provider API lookup, etc.

Set HC_BASE_URL to point clients at a remote deployment.
"""
import os
import requests


BASE_URL = os.environ.get("HC_BASE_URL", "http://127.0.0.1:5000")
DEFAULT_TIMEOUT = float(os.environ.get("HC_SERVICE_TIMEOUT", "5"))


class ServiceError(Exception):
    """Raised when a downstream service call fails."""

    def __init__(self, service, status, message):
        super().__init__(f"[{service}] {status}: {message}")
        self.service = service
        self.status = status
        self.message = message

    def to_response(self):
        code = self.status if isinstance(self.status, int) and 400 <= self.status < 600 else 502
        # Surface an upstream 404 as a 400 for the client of the calling service,
        # because it means the caller referenced something that doesn't exist.
        if code == 404:
            code = 400
        return {
            "error": f"dependency '{self.service}' failed",
            "status": self.status,
            "detail": self.message,
        }, code


class ServiceClient:
    def __init__(self, name, base_path):
        self.name = name
        self.base_path = base_path

    def _url(self, path=""):
        return f"{BASE_URL}{self.base_path}{path}"

    def _handle(self, response):
        if response.status_code >= 400:
            try:
                detail = response.json()
            except ValueError:
                detail = response.text
            raise ServiceError(self.name, response.status_code, detail)
        return response.json()

    def get(self, path="", params=None):
        try:
            r = requests.get(self._url(path), params=params, timeout=DEFAULT_TIMEOUT)
        except requests.RequestException as e:
            raise ServiceError(self.name, "connection_error", str(e))
        return self._handle(r)

    def post(self, path, json=None):
        try:
            r = requests.post(self._url(path), json=json, timeout=DEFAULT_TIMEOUT)
        except requests.RequestException as e:
            raise ServiceError(self.name, "connection_error", str(e))
        return self._handle(r)

    def patch(self, path, json=None):
        try:
            r = requests.patch(self._url(path), json=json, timeout=DEFAULT_TIMEOUT)
        except requests.RequestException as e:
            raise ServiceError(self.name, "connection_error", str(e))
        return self._handle(r)

    def delete(self, path):
        try:
            r = requests.delete(self._url(path), timeout=DEFAULT_TIMEOUT)
        except requests.RequestException as e:
            raise ServiceError(self.name, "connection_error", str(e))
        return self._handle(r)


patients_svc = ServiceClient("patients", "/api/patients")
providers_svc = ServiceClient("providers", "/api/providers")
appointments_svc = ServiceClient("appointments", "/api/appointments")
ehr_svc = ServiceClient("ehr", "/api/ehr")
lab_svc = ServiceClient("lab", "/api/lab")
imaging_svc = ServiceClient("imaging", "/api/imaging")
pharmacy_svc = ServiceClient("pharmacy", "/api/pharmacy")
insurance_svc = ServiceClient("insurance", "/api/insurance")
claims_svc = ServiceClient("claims", "/api/claims")
invoices_svc = ServiceClient("invoices", "/api/invoices")
payments_svc = ServiceClient("payments", "/api/payments")
notifications_svc = ServiceClient("notifications", "/api/notifications")
devices_svc = ServiceClient("devices", "/api/devices")
ai_agents_svc = ServiceClient("ai_agents", "/api/ai-agents")


def require(service, resource_id, kind):
    """Fetch a record from a downstream service; return the record or raise ServiceError."""
    if resource_id is None:
        raise ServiceError(service.name, 400, f"{kind}_id is required")
    return service.get(f"/{resource_id}")
