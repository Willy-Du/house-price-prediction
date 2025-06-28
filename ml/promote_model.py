import mlflow

client = mlflow.tracking.MlflowClient()

# Récupère toutes les versions
versions = client.search_model_versions("name='house-price-model'")

# Filtre la plus récente version
latest = sorted(versions, key=lambda v: int(v.version))[-1]

# Promotion
client.transition_model_version_stage(
    name=latest.name,
    version=latest.version,
    stage="Production",
    archive_existing_versions=True
)

print(f"✅ {latest.name} version {latest.version} promoted to Production.")
