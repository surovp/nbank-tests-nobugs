#!/usr/bin/env bash
set -euo pipefail

CHART_DIR="./nbank-charts"
RELEASE_NAME="nbank"
NAMESPACE="default"

# ---------- ШАГ 1: запуск Minikube ----------
echo "🚀 Запускаем Minikube..."
minikube start --driver=docker

# ---------- ШАГ 2: установка Helm-чарта ----------
echo "📦 Устанавливаем Helm-чарт ${RELEASE_NAME}..."
helm install "${RELEASE_NAME}" "${CHART_DIR}" --namespace "${NAMESPACE}" || \
    helm upgrade "${RELEASE_NAME}" "${CHART_DIR}" --namespace "${NAMESPACE}"

# ---------- ШАГ 3: ждём готовности подов ----------
echo "⏳ Ждём готовности подов (до 120 секунд)..."
kubectl wait --for=condition=Ready pod -l app=postgres --timeout=120s || true
kubectl wait --for=condition=Ready pod -l app=backend  --timeout=120s || true
kubectl wait --for=condition=Ready pod -l app=frontend --timeout=120s || true

# ---------- ШАГ 4: показываем состояние ----------
echo ""
echo "📋 Сервисы:"
kubectl get svc

echo ""
echo "📋 Поды:"
kubectl get pods

# ---------- ШАГ 5: логи backend ----------
echo ""
echo "📜 Логи backend (последние 30 строк):"
kubectl logs deployment/backend --tail=30 || true

# ---------- ШАГ 6: проброс портов ----------
echo ""
echo "🔌 Пробрасываем порты..."
echo "  backend  → http://localhost:4111"
echo "  frontend → http://localhost:3000"
echo ""
echo "Для остановки нажмите Ctrl+C"

# Проброс портов в фоне
kubectl port-forward svc/backend  4111:4111 > /dev/null 2>&1 &
BACKEND_PID=$!

kubectl port-forward svc/frontend 3000:80   > /dev/null 2>&1 &
FRONTEND_PID=$!

# Ждём, пока пользователь не нажмёт Ctrl+C
trap "echo ''; echo '🛑 Останавливаем проброс портов...'; kill ${BACKEND_PID} ${FRONTEND_PID} 2>/dev/null || true" EXIT
wait