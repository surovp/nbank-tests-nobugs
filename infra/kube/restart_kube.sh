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
sleep 5
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

# ---------- ШАГ 9: установка мониторинга ----------
echo ""
echo "═══════════════════════════════════════════════"
echo "📊 Устанавливаем Prometheus + Grafana"
echo "═══════════════════════════════════════════════"

helm repo add prometheus-community https://prometheus-community.github.io/helm-charts || true
helm repo add elastic https://helm.elastic.co || true
helm repo update

helm upgrade --install monitoring prometheus-community/kube-prometheus-stack -n monitoring --create-namespace -f monitoring-values.yaml

# Ждём готовности Prometheus
echo ""
sleep 5
echo "⏳ Ждём готовности Prometheus (до 300 секунд)..."
kubectl wait --for=condition=Ready pod \
  -l app.kubernetes.io/name=prometheus \
  -n monitoring --timeout=300s

# Ждём готовности Grafana
echo "⏳ Ждём готовности Grafana..."
kubectl wait --for=condition=Ready pod \
  -l app.kubernetes.io/name=grafana \
  -n monitoring --timeout=180s

# Пробрасываем порт к прометеусу и графане
echo ""
echo "▶️  kubectl port-forward svc/monitoring-kube-prometheus-prometheus -n monitoring 3001:9090"
kubectl port-forward svc/monitoring-kube-prometheus-prometheus -n monitoring 3001:9090 > /tmp/prometheus-pf.log 2>&1 &
PROMETHEUS_PID=$!

echo "▶️  kubectl port-forward svc/monitoring-grafana -n monitoring 3002:80"
kubectl port-forward svc/monitoring-grafana -n monitoring 3002:80 > /tmp/grafana-pf.log 2>&1 &
GRAFANA_PID=$!

# Создаем секреты для авторизации на бекенде
kubectl create secret generic backend-basic-auth --from-literal=username=admin --from-literal=password=admin -n monitoring || true

# Применяем yaml с настройкой SpringMonitoring за бекендом
kubectl apply -f spring-monitoring.yaml

# Обновляем trap — добавляем PID'ы мониторинга
trap "echo ''; echo '🛑 Останавливаем проброс портов...'; kill ${BACKEND_PID:-} ${FRONTEND_PID:-} ${PROMETHEUS_PID:-} ${GRAFANA_PID:-} ${KIBANA_PID:-} 2>/dev/null || true" EXIT

# ---------- ШАГ 10: логирование (Elasticsearch + Kibana + Fluent Bit) ----------
echo ""
echo "═══════════════════════════════════════════════"
echo "📝 Устанавливаем стек логирования (EFK)"
echo "═══════════════════════════════════════════════"

# Elasticsearch из elastic-чарта (уже установлен, обновляем)
helm upgrade --install elasticsearch elastic/elasticsearch \
  -n logging --create-namespace \
  --set replicas=1 \
  --set persistence.enabled=false \
  --set resources.requests.memory=1Gi \
  --set resources.limits.memory=1Gi

# Ждём готовности Elasticsearch
echo "⏳ Ждём готовности Elasticsearch (до 300 секунд)..."
kubectl wait --for=condition=Ready pod elasticsearch-master-0 \
  -n logging --timeout=300s

# Скачиваем Kibana-чарт с GitHub (обход 403 на helm.elastic.co)
echo "📥 Скачиваем Kibana-чарт с GitHub..."
if [ ! -d /tmp/helm-charts ]; then
  git clone --depth=1 https://github.com/elastic/helm-charts.git /tmp/helm-charts
fi

# Kibana из локального чарта
helm upgrade --install kibana /tmp/helm-charts/kibana \
  -n logging \
  --set service.type=NodePort

# Ждём готовности Kibana
echo "⏳ Ждём готовности Kibana..."
kubectl wait --for=condition=Ready pod -l app=kibana \
  -n logging --timeout=300s

# Получаем пароль Elasticsearch из Secret
ES_PASSWORD=$(kubectl get secret elasticsearch-master-credentials -n logging \
  -o jsonpath='{.data.password}' | base64 -d)

# Создаём Secret для Fluent Bit
kubectl create secret generic fluent-bit-es-credentials \
  --from-literal=ES_PASSWORD="$ES_PASSWORD" \
  -n logging \
  --dry-run=client -o yaml | kubectl apply -f -

# Fluent Bit — собирает логи контейнеров и шлёт в Elasticsearch
helm repo add fluent https://fluent.github.io/helm-charts || true
helm repo update
helm upgrade --install fluent-bit fluent/fluent-bit \
  -n logging \
  -f fluent-bit-values.yaml

# Проброс порта Kibana
echo "▶️  kubectl port-forward svc/kibana-kibana -n logging 5601:5601"
kubectl port-forward svc/kibana-kibana -n logging 5601:5601 > /tmp/kibana-pf.log 2>&1 &
KIBANA_PID=$!

# Обновляем trap — добавляем Kibana
trap "echo ''; echo '🛑 Останавливаем проброс портов...'; kill ${BACKEND_PID:-} ${FRONTEND_PID:-} ${PROMETHEUS_PID:-} ${GRAFANA_PID:-} ${KIBANA_PID:-} 2>/dev/null || true" EXIT

# ---------- Финал ----------
echo ""
echo "═══════════════════════════════════════════════"
echo "🎉 Окружение успешно развёрнуто и доступно!"
echo "═══════════════════════════════════════════════"
echo ""
echo "  Backend    → http://localhost:4111"
echo "  Frontend   → http://localhost:3000"
echo "  Prometheus → http://localhost:3001"
echo "  Grafana    → http://localhost:3002"
echo "  Kibana     → http://localhost:5601"
echo ""
echo "Для остановки нажмите Ctrl+C"

wait