# ============================================================
# schemas.py — Définition des données entrées / sorties
# ============================================================
# Pydantic valide automatiquement les types
# Si quelqu'un envoie une string à la place d'un float → erreur claire

from pydantic import BaseModel, Field
from typing import Literal

class SensorInput(BaseModel):
    """
    Données capteur envoyées par l'application OCP
    """
    air_temp_k:          float = Field(..., ge=250, le=400, 
                                description="Température air en Kelvin")
    process_temp_k:      float = Field(..., ge=250, le=400,
                                description="Température process en Kelvin")
    rotation_speed_rpm:  float = Field(..., ge=100, le=5000,
                                description="Vitesse rotation en RPM")
    torque_nm:           float = Field(..., ge=0,   le=200,
                                description="Couple en Newton-mètre")
    tool_wear_min:       float = Field(..., ge=0,
                                description="Usure outil en minutes")
    station_type:        Literal["L", "M", "H"] = Field(...,
                                description="Type de station")

    # Exemple affiché dans la documentation automatique FastAPI
    class Config:
        json_schema_extra = {
            "example": {
                "air_temp_k":         298.5,
                "process_temp_k":     308.7,
                "rotation_speed_rpm": 1551.0,
                "torque_nm":          42.8,
                "tool_wear_min":      108.0,
                "station_type":       "M"
            }
        }

class PredictionOutput(BaseModel):
    """
    Réponse retournée par l'API
    """
    failure_predicted:  bool
    failure_type:       str
    probability:        float
    risk_level:         Literal["LOW", "MEDIUM", "HIGH"]
    recommendation:     str