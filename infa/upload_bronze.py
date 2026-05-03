import os
from azure.storage.filedatalake import DataLakeServiceClient
from azure.identity import DefaultAzureCredential

ACCOUNT_NAME = "datalakeocp2026"
CONTAINER_NAME = "bronse"

# Les 2 fichiers à uploader
FILES = [
    {
        "local": r"C:\Users\DELL£\Downloads\projet ocp\Data\ai4i2020.csv",
        "target": "sensors_raw/ai4i2020.csv"
    },
    {
        "local": r"C:\Users\DELL£\Downloads\projet ocp\Data\predictive_maintenance_v3.csv",
        "target": "sensors_raw/predictive_maintenance_v3.csv"
    }
]

print("Connexion à Azure...")
credential = DefaultAzureCredential()
account_url = f"https://{ACCOUNT_NAME}.dfs.core.windows.net"
service_client = DataLakeServiceClient(account_url, credential=credential)
fs_client = service_client.get_file_system_client(CONTAINER_NAME)

for f in FILES:
    print(f"Upload : {f['local']} ...")
    file_client = fs_client.get_file_client(f["target"])
    with open(f["local"], "rb") as data:
        file_client.upload_data(data, overwrite=True)
    print(f"✅ {f['target']} uploadé !")

print("\n🎉 Ingestion Bronze terminée !")