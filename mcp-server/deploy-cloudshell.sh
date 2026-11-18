#!/usr/bin/env bash
# Instala o actualiza el MCP propio de Odoo en Google Cloud Run.
# Correr en Google Cloud Shell, dentro de la carpeta descomprimida del paquete:
#   bash deploy-cloudshell.sh
set -euo pipefail

PROJECT="${PROJECT:-ventasguate-mcp}"
REGION="${REGION:-us-central1}"
SERVICE="odoo-mcp-vg"
ODOO_URL="https://ventasguate.odoo.com"
ODOO_DB="rocketgithub-ventasguate-odoo-sh-main-5436798"

echo "== 1/6 Proyecto $PROJECT"
gcloud config set project "$PROJECT" >/dev/null
PN=$(gcloud projects describe "$PROJECT" --format='value(projectNumber)')
SA="$PN-compute@developer.gserviceaccount.com"

echo "== 2/6 Activando servicios (tarda 1-2 min la primera vez)"
gcloud services enable run.googleapis.com cloudbuild.googleapis.com artifactregistry.googleapis.com secretmanager.googleapis.com

echo "== 3/6 Clave secreta del servidor"
if ! gcloud secrets describe odoo-mcp-secret >/dev/null 2>&1; then
  python3 -c "import base64,os;print(base64.urlsafe_b64encode(os.urandom(32)).decode(),end='')" \
    | gcloud secrets create odoo-mcp-secret --replication-policy=automatic --data-file=-
fi
gcloud secrets add-iam-policy-binding odoo-mcp-secret --member="serviceAccount:$SA" \
  --role=roles/secretmanager.secretAccessor >/dev/null

echo "== 4/6 Permisos de compilación"
for ROLE in roles/cloudbuild.builds.builder roles/artifactregistry.writer roles/logging.logWriter roles/storage.objectViewer; do
  gcloud projects add-iam-policy-binding "$PROJECT" --member="serviceAccount:$SA" --role="$ROLE" --condition=None >/dev/null
done

echo "== 5/6 Compilando y publicando (3-5 min)"
gcloud run deploy "$SERVICE" --source . --region "$REGION" --quiet \
  --no-invoker-iam-check --min-instances 0 --max-instances 2 --memory 512Mi \
  --set-env-vars "ODOO_URL=$ODOO_URL,ODOO_DB=$ODOO_DB,MCP_ALLOW_WRITE=0" \
  --set-secrets "MCP_SECRET_KEY=odoo-mcp-secret:latest"
URL=$(gcloud run services describe "$SERVICE" --region "$REGION" --format='value(status.url)')
gcloud run services update "$SERVICE" --region "$REGION" --quiet --update-env-vars "MCP_PUBLIC_URL=$URL" >/dev/null

echo "== 6/6 Verificación"
sleep 5
H=$(curl -s -o /dev/null -w '%{http_code}' "$URL/health")
M=$(curl -s "$URL/.well-known/oauth-authorization-server" | grep -c registration_endpoint || true)
U=$(curl -s -o /dev/null -w '%{http_code}' -X POST "$URL/mcp")
echo "salud: $H (esperado 200) · OAuth publicado: $M (esperado 1) · /mcp sin sesión: $U (esperado 401)"
echo
echo "================================================================"
echo " LISTO. URL del conector para claude.ai:"
echo "   $URL/mcp"
echo "================================================================"
