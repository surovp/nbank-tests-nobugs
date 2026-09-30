#!/usr/bin/env bash
set -euo pipefail

# ---------- Настройки ----------
COMPOSE_FILE="infra/docker-compose/docker-compose.yaml"
TEST_IMAGE="python-tests:with-stab-tests"
NETWORK_NAME="docker-compose_nbank-network"

ENV_FILE=".env.ci"           # окружение для тест-контейнера
ENV_VERSIONS=".env.versions" # версии backend/frontend для compose

API_MARKER="api"
UI_MARKER="ui"
API_VERSION="with_database_with_fix_with_swagger"

# ---------- Проверки ----------
if [[ ! -f "${COMPOSE_FILE}" ]]; then
  echo "❌ Не найден файл docker compose: ${COMPOSE_FILE}"
  exit 1
fi

if [[ ! -f "${ENV_FILE}" ]]; then
  echo "❌ Не найден файл окружения: ${ENV_FILE}"
  exit 1
fi

if [[ ! -f "${ENV_VERSIONS}" ]]; then
  echo "❌ Не найден файл версий: ${ENV_VERSIONS}"
  exit 1
fi

if ! docker image inspect "${TEST_IMAGE}" >/dev/null 2>&1; then
  echo "❌ Локальный образ '${TEST_IMAGE}' не найден."
  exit 1
fi

# ---------- Гарантированная остановка окружения ----------
cleanup() {
  echo ""
  echo "🧹 Останавливаем тестовое окружение..."
  docker compose --env-file "${ENV_VERSIONS}" -f "${COMPOSE_FILE}" down -v >/dev/null 2>&1 || true
  echo "✅ Окружение остановлено."
}
trap cleanup EXIT

# ---------- 1. Поднимаем окружение ----------
echo "🚀 Поднимаем тестовое окружение..."
docker compose --env-file "${ENV_VERSIONS}" -f "${COMPOSE_FILE}" up -d

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
  --env-file "${ENV_FILE}" \
  "${TEST_IMAGE}" \
  pytest -m "${API_MARKER}" --api-version "${API_VERSION}"

# ---------- 4. Запускаем UI-тесты ----------
echo ""
echo "=============================================="
echo " 🧪 Запуск UI-тестов"
echo "=============================================="
docker run --rm \
  --network "${NETWORK_NAME}" \
  -p 8080:8080 \
  --env-file "${ENV_FILE}" \
  "${TEST_IMAGE}" \
  pytest -m "${UI_MARKER}"

echo ""
echo "✅ Все тесты завершены успешно!"