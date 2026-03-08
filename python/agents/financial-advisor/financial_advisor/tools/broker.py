import os, time, json, hashlib
import requests

BROKER_URL = os.getenv("MOCK_BROKER_URL", "http://localhost:8099/broker/place_order")
DEMO_SIDE_EFFECTS = os.getenv("DEMO_SIDE_EFFECTS", "0") == "1"
KYB_REQUIRED = os.getenv("KYB_DEMO_FAIL_CLOSED", "0") == "1"

def _fail_closed_guard():
    # "Unavoidable" demo mode: side effects cannot run unless Kybernis routing is active
    if not (DEMO_SIDE_EFFECTS and KYB_REQUIRED):
        return
    # minimal proof of “Kybernis engaged”: require proxy envs OR explicit KYB_ON
    if os.getenv("KYB_ON") != "1":
        raise RuntimeError("KYB_DEMO_FAIL_CLOSED: KYB_ON=1 required to execute side-effects")
    if not (os.getenv("HTTP_PROXY") or os.getenv("HTTPS_PROXY")):
        raise RuntimeError("KYB_DEMO_FAIL_CLOSED: HTTP(S)_PROXY must route through Kybernis proxy")

def broker_place_order(payload: dict) -> dict:
    """
    Side-effect: "place order" (charge-like operation)
    Intentionally includes naive retries to demonstrate duplication without Kybernis.
    """
    _fail_closed_guard()

    timeout_s = float(os.getenv("BROKER_TIMEOUT_S", "1.5"))
    retries = int(os.getenv("BROKER_RETRIES", "1"))  # set 1 to show duplication (attempt 1 + retry 1 = 2)
    backoff_ms = int(os.getenv("BROKER_BACKOFF_MS", "200"))

    # Important: DO NOT do semantic caching.
    # The idempotency is handled by Kybernis proxy based on headers derived from execution span.
    headers = {"Content-Type": "application/json"}

    last_err = None
    for attempt in range(retries + 1):
        try:
            r = requests.post(BROKER_URL, headers=headers, data=json.dumps(payload), timeout=timeout_s)
            r.raise_for_status()
            return {"ok": True, "status_code": r.status_code, "body": r.json()}
        except Exception as e:
            last_err = str(e)
            if attempt < retries:
                time.sleep(backoff_ms / 1000.0)
                continue
            return {"ok": False, "error": last_err}
