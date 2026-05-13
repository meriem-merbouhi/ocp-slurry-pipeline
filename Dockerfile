# ============================================================
# Dockerfile — Container OCP Predictive API
# ============================================================

# Image de base légère Python
FROM python:3.11-slim

# Répertoire de travail dans le container
WORKDIR /app

# Copier les dépendances en premier (optimisation cache Docker)
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier tout le code
COPY . .

# Port exposé par l'API
EXPOSE 8000

# Commande de démarrage
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]