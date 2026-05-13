# ============================================================
# main.py — API FastAPI OCP Slurry Pipeline
# ============================================================

from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
from app.schemas import SensorInput, PredictionOutput
from app.model  import predict
from datetime   import datetime

app = FastAPI(
    title       = "OCP Slurry Pipeline — Predictive Maintenance API",
    description = "API de maintenance prédictive pour les pompes OCP",
    version     = "1.0.0",
    docs_url    = None  # on désactive le docs par défaut
)

@app.get("/docs", include_in_schema=False)
def custom_swagger():
    return get_swagger_ui_html(
        openapi_url     = "/openapi.json",
        title           = "OCP API Docs",
        swagger_js_url  = "https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url = "https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css"
    )
# ─────────────────────────────────────────
# GET /health — vérifier que l'API fonctionne
# ─────────────────────────────────────────
@app.get("/health")
def health_check():
    """
    Endpoint de santé — utilisé par Azure pour vérifier
    que le container est vivant
    """
    return {
        "status":    "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version":   "1.0.0"
    }

# ─────────────────────────────────────────
# GET /model-info — informations sur le modèle
# ─────────────────────────────────────────
@app.get("/model-info")
def model_info():
    """
    Informations sur le modèle déployé
    """
    return {
        "model_name":    "OCP Predictive Maintenance",
        "model_version": "1.0-rules-based",
        "features":      ["air_temp_k", "process_temp_k", 
                         "rotation_speed_rpm", "torque_nm", 
                         "tool_wear_min", "station_type"],
        "target":        "failure_type",
        "classes":       ["NONE", "TWF", "HDF", "PWF", "OSF", "RNF"],
        "note":          "Modèle ML complet disponible en v2.0"
    }

# ─────────────────────────────────────────
# POST /predict — prédiction principale
# ─────────────────────────────────────────
@app.post("/predict", response_model=PredictionOutput)
def predict_failure(sensor_data: SensorInput):
    """
    Prédit le type de panne à partir des données capteur.

    Envoie les mesures en temps réel →
    Reçois une prédiction avec niveau de risque et recommandation
    """
    return predict(sensor_data)