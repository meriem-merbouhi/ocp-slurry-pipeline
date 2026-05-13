# test_api.py — Tester l'API OCP
import urllib.request
import json

BASE_URL = "http://127.0.0.1:8000"

# ── Test 1 : Health ──────────────────────
print("=" * 40)
print("TEST 1 — /health")
req = urllib.request.urlopen(f"{BASE_URL}/health")
print(json.loads(req.read()))

# ── Test 2 : Cas normal ──────────────────
print("\nTEST 2 — Capteur normal")
data = json.dumps({
    "air_temp_k":         298.5,
    "process_temp_k":     308.7,
    "rotation_speed_rpm": 1551.0,
    "torque_nm":          42.8,
    "tool_wear_min":      108.0,
    "station_type":       "M"
}).encode()

req = urllib.request.Request(
    f"{BASE_URL}/predict",
    data    = data,
    headers = {"Content-Type": "application/json"},
    method  = "POST"
)
result = json.loads(urllib.request.urlopen(req).read())
print(f"Panne prédite  : {result['failure_predicted']}")
print(f"Type           : {result['failure_type']}")
print(f"Risque         : {result['risk_level']}")
print(f"Recommandation : {result['recommendation']}")

# ── Test 3 : Panne simulée ───────────────
print("\nTEST 3 — Panne HDF simulée (temp_diff faible)")
data = json.dumps({
    "air_temp_k":         298.5,
    "process_temp_k":     298.6,
    "rotation_speed_rpm": 1551.0,
    "torque_nm":          42.8,
    "tool_wear_min":      108.0,
    "station_type":       "H"
}).encode()

req = urllib.request.Request(
    f"{BASE_URL}/predict",
    data    = data,
    headers = {"Content-Type": "application/json"},
    method  = "POST"
)
result = json.loads(urllib.request.urlopen(req).read())
print(f"Panne prédite  : {result['failure_predicted']}")
print(f"Type           : {result['failure_type']}")
print(f"Risque         : {result['risk_level']}")
print(f"Recommandation : {result['recommendation']}")