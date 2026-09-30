set -euo pipefail

# Автозагрузка .env, если файл есть рядом со скриптом
if [[ -f .env ]]; then
   set -a
   source .env
   set +a
fi

# Токен обязателен — либо из .env, либо из окружения
: "${DOCKERHUB_TOKEN:?Не задан DOCKERHUB_TOKEN. Положите его в .env рядом со скриптом или сделайте export в ~/.bashrc}"

# Публикация локально собранного образа с тестами в Docker Hub.
# Все параметры вводятся вручную после запуска скрипта.

echo "=============================================="
echo " Публикация образа с тестами в Docker Hub"
echo "=============================================="
echo ""

# --- Ввод данных ---
read -r -p "Имя локального образа (например, python-tests:first-dockerfile): " LOCAL_IMAGE 
[[ -n "${LOCAL_IMAGE}" ]] || { echo "❌ Имя локального образа не может быть пустым."; exit 1; }

read -r -p "Ваш логин на Docker Hub: " DOCKERHUB_USER
[[ -n "${DOCKERHUB_USER}" ]] || { echo "❌ Логин Docker Hub не может быть пустым."; exit 1; }

read -r -p "Имя репозитория на Docker Hub (например, nbank-tests): " IMAGE_NAME
[[ -n "${IMAGE_NAME}" ]] || { echo "❌ Имя репозитория не может быть пустым."; exit 1; }

read -r -p "Тег (например, latest): " TAG
[[ -n "${TAG}" ]] || { echo "❌ Тег не может быть пустым."; exit 1; }

# --- Формируем полное имя образа: <user>/<image>:<tag> ---
FULL_IMAGE="${DOCKERHUB_USER}/${IMAGE_NAME}:${TAG}"

echo ""
echo "=============================================="
echo " Локальный образ : ${LOCAL_IMAGE}"
echo " Целевой образ   : ${FULL_IMAGE}"
echo "=============================================="
echo ""

read -r -p "Всё верно? Продолжить? [y/N]: " CONFIRM
[[ "${CONFIRM}" =~ ^[Yy]$ ]] || { echo "Отменено."; exit 0; }

# --- Проверка, что локальный образ существует ---
if ! docker image inspect "${LOCAL_IMAGE}" >/dev/null 2>&1; then
   echo "❌ Локальный образ '${LOCAL_IMAGE}' не найден."
   echo "   Соберите его: docker build -t ${LOCAL_IMAGE} ."
   exit 1
fi

# --- Логин в Docker Hub (токен подключим позже) ---
echo "🔐 Логин в Docker Hub как '${DOCKERHUB_USER}'..."
echo "${DOCKERHUB_TOKEN}" | docker login -u "${DOCKERHUB_USER}" --password-stdin

# --- Тегирование и пуш ---
echo "🏷️  Тегируем: ${LOCAL_IMAGE}  →  ${FULL_IMAGE}"
docker tag "${LOCAL_IMAGE}" "${FULL_IMAGE}"

echo "🚀 Публикуем в Docker Hub: ${FULL_IMAGE}"
docker push "${FULL_IMAGE}"

# --- Итог ---
echo ""
echo "✅ Готово! Образ опубликован: ${FULL_IMAGE}"
echo ""
echo "Скачать образ командой:"
echo "docker pull ${FULL_IMAGE}"
echo ""
echo "Проверить на Docker Hub:"
echo "https://hub.docker.com/r/${DOCKERHUB_USER}/${IMAGE_NAME}"
