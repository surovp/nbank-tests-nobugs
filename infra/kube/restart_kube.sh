#!/usr/bin/env bash
set -euo pipefail

CHART_DIR="./nbank-charts"
RELEASE_NAME="nbank"
NAMESPACE="default"

# ---------- ШАГ 1: запуск Minikube ----------
echo "🚀 Запускаем Minikube..."
minikube start --driver=docker

# ---------- ШАГ 2: секреты ----------
echo "🔐 Создаём Secret для Postgres..."
kubectl create secret generic postgres-secret \
  --from-literal=username=postgres \
  --from-literal=password=postgres \
  -n "${NAMESPACE}" \
  --dry-run=client -o yaml | kubectl apply -f -

# ---------- ШАГ 3: установка Helm-чарта ----------
echo "📦 Устанавливаем Helm-чарт ${RELEASE_NAME}..."
helm install "${RELEASE_NAME}" "${CHART_DIR}" --namespace "${NAMESPACE}" || \
    helm upgrade "${RELEASE_NAME}" "${CHART_DIR}" --namespace "${NAMESPACE}"

# ---------- ШАГ 4: ждём готовности ----------
echo ""
echo "⏳ Ждём готовности подов (до 120 секунд)..."
kubectl wait --for=condition=Ready pod -l app=postgres --timeout=120s
kubectl wait --for=condition=Ready pod -l app=backend  --timeout=120s
kubectl wait --for=condition=Ready pod -l app=frontend --timeout=120s

# ---------- ШАГ 5: состояние кластера ----------
echo ""
echo "═══════════════════════════════════════════════"
echo "📋 Состояние кластера"
echo "═══════════════════════════════════════════════"

echo ""
echo "───── Сервисы ─────"
kubectl get svc

echo ""
echo "───── Поды ─────"
kubectl get pods

echo ""
echo "───── ConfigMap ─────"
kubectl get configmap

echo ""
echo "───── Secret ─────"
kubectl get secret

# ---------- ШАГ 6: логи всех сервисов ----------
echo ""
echo "═══════════════════════════════════════════════"
echo "📜 Логи сервисов"
echo "═══════════════════════════════════════════════"

echo ""
echo "───── Postgres (последние 20 строк) ─────"
kubectl logs deployment/postgres --tail=20 || true

echo ""
echo "───── Backend (последние 30 строк) ─────"
kubectl logs deployment/backend --tail=30 || true

echo ""
echo "───── Frontend (последние 20 строк) ─────"
kubectl logs deployment/frontend --tail=20 || true

# ---------- ШАГ 7: проброс портов ----------
echo ""
echo "═══════════════════════════════════════════════"
echo "🔌 Пробрасываем порты"
echo "═══════════════════════════════════════════════"
echo "  backend  → http://localhost:4111"
echo "  frontend → http://localhost:3000"
echo ""
echo "Для остановки нажмите Ctrl+C"

kubectl port-forward svc/backend  4111:4111 > /dev/null 2>&1 &
BACKEND_PID=$!

kubectl port-forward svc/frontend 3000:80   > /dev/null 2>&1 &
FRONTEND_PID=$!

trap "echo ''; echo '🛑 Останавливаем проброс портов...'; kill ${BACKEND_PID} ${FRONTEND_PID} 2>/dev/null || true" EXIT


# ---------- ШАГ 8: проверка доступности ----------
echo ""
echo "⏳ Ждём, пока port-forward установится..."
sleep 3

echo ""
echo "───── Проверка backend ─────"
if curl -sf http://localhost:4111/actuator/health > /tmp/backend_health.json; then
    echo "✅ Backend доступен: http://localhost:4111"
    echo "   Ответ: $(cat /tmp/backend_health.json)"
else
    echo "❌ Backend НЕ отвечает на http://localhost:4111/actuator/health"
    exit 1
fi

echo ""
echo "───── Проверка frontend ─────"
if curl -sfI http://localhost:3000 > /tmp/frontend_head.txt; then
    echo "✅ Frontend доступен: http://localhost:3000"
    echo "   Ответ: $(head -1 /tmp/frontend_head.txt)"
else
    echo "❌ Frontend НЕ отвечает на http://localhost:3000"
    exit 1
fi

# ---------- Финал ----------
echo ""
echo "═══════════════════════════════════════════════"
echo "🎉 Окружение успешно развёрнуто и доступно!"
echo "═══════════════════════════════════════════════"
echo ""
echo "  Backend  → http://localhost:4111"
echo "  Frontend → http://localhost:3000"
echo ""
echo "Для остановки нажмите Ctrl+C"

wait