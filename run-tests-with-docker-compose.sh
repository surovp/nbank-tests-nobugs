#!/usr/bin/env bash
set -euo pipefail

# ============================================================
#  run-tests-with-docker-compose.sh
#  Поднимает окружение, запускает API и UI тесты, гасит окружение.
# ============================================================

# ---------- Настройки ----------
COMPOSE_FILE="infra/docker-compose/docker-compose.yaml"
TEST_IMAGE="python-tests:first-dockerfile"

# Имя compose-сети
NETWORK_NAME="docker-compose_nbank-network"

# Адреса сервисов внутри compose-сети (по именам сервисов)
BACKEND_URL="http://backend:4111/api/v1"
UI_BASE_URL="http://frontend:80"

API_MARKER="api"
UI_MARKER="ui"
API_VERSION="with_fraud_check"

# ---------- Проверки ----------
if [[ ! -f "${COMPOSE_FILE}" ]]; then
  echo "❌ Не найден файл docker compose: ${COMPOSE_FILE}"
  exit 1
fi

if ! docker image inspect "${TEST_IMAGE}" >/dev/null 2>&1; then
  echo "❌ Локальный образ '${TEST_IMAGE}' не найден."
  exit 1
fi

cleanup() {
  echo ""
  echo "🧹 Останавливаем тестовое окружение..."
  docker compose -f "${COMPOSE_FILE}" down -v >/dev/null 2>&1 || true
  echo "✅ Окружение остановлено."
}
trap cleanup EXIT

# ---------- 1. Поднимаем окружение ----------
echo "🚀 Поднимаем тестовое окружение..."
docker compose -f "${COMPOSE_FILE}" up -d

# ---------- 2. Ждём готовности backend ----------
echo "⏳ Ждём готовности backend..."
for i in $(seq 1 60); do
  if curl -sf http://localhost:4111/actuator/health >/dev/null 2>&1; then
    echo "✅ Backend готов."
    break
  fi
  if [[ "${i}" -eq 60 ]]; then
    echo "❌ Backend не поднялся за 60 секунд."
    exit 1
  fi
  sleep 1
done

# ---------- 3. Запускаем API-тесты ----------
echo ""
echo "=============================================="
echo " 🧪 Запуск API-тестов"
echo "=============================================="
docker run --rm \
  --name fraud-mock \
  --network "${NETWORK_NAME}" \
  -p 8080:8080 \
  -e BACKEND_URL="${BACKEND_URL}" \
  -e UI_BASE_URL="${UI_BASE_URL}" \
  -e PLAYWRIGHT_TEST_BASE_URL="${UI_BASE_URL}" \
  "${TEST_IMAGE}" \
  pytest -m api --api-version "${API_VERSION}"

# ---------- 4. Запускаем UI-тесты ----------
echo ""
echo "=============================================="
echo " 🧪 Запуск UI-тестов"
echo "=============================================="
docker run --rm \
  --network "${NETWORK_NAME}" \
  -p 8080:8080 \
  -e BACKEND_URL="${BACKEND_URL}" \
  -e UI_BASE_URL="${UI_BASE_URL}" \
  -e PLAYWRIGHT_TEST_BASE_URL="${UI_BASE_URL}" \
  "${TEST_IMAGE}" \
  pytest -m ui

echo ""
echo "✅ Все тесты завершены."