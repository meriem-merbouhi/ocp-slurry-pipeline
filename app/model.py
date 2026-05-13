# ============================================================
# model.py — Gestion du modèle ML
# ============================================================
# Pour l'instant : modèle simulé (règles physiques)
# En J11 : remplacé par le vrai modèle XGBoost/Random Forest

import numpy as np
from app.schemas import SensorInput, PredictionOutput

def predict(data: SensorInput) -> PredictionOutput:
    """
    Simulation du modèle ML avec règles physiques OCP
    En J11 : joblib.load('models/model.pkl').predict(features)
    """

    # Feature engineering simplifié (comme en J6)
    temp_diff        = data.process_temp_k - data.air_temp_k
    power_estimated  = data.torque_nm * (data.rotation_speed_rpm * 2 * np.pi / 60)
    tool_wear_rate   = data.tool_wear_min / max(data.rotation_speed_rpm, 1)

    # Règles de détection (simulées en attendant le vrai modèle J11)
    failure_type = "NONE"
    probability  = 0.05

    # Tool Wear Failure
    if data.tool_wear_min > 200:
        failure_type = "TWF"
        probability  = min(0.95, data.tool_wear_min / 250)

    # Heat Dissipation Failure
    elif temp_diff < 8.6:
        failure_type = "HDF"
        probability  = max(0.60, 1 - temp_diff / 10)

    # Power Failure
    elif power_estimated < 3500 or power_estimated > 9000:
        failure_type = "PWF"
        probability  = 0.72

    # Overstrain Failure
    elif data.torque_nm > 65 and data.rotation_speed_rpm < 1380:
        failure_type = "OSF"
        probability  = 0.81

    # Niveau de risque
    if probability < 0.3:
        risk_level = "LOW"
        recommendation = "Fonctionnement normal — surveillance standard"
    elif probability < 0.7:
        risk_level = "MEDIUM"
        recommendation = "Attention requise — vérification dans 24h"
    else:
        risk_level = "HIGH"
        recommendation = "INTERVENTION URGENTE — arrêt préventif recommandé"

    return PredictionOutput(
        failure_predicted = failure_type != "NONE",
        failure_type      = failure_type,
        probability       = round(probability, 4),
        risk_level        = risk_level,
        recommendation    = recommendation
    )