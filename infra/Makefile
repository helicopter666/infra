# ═══════════════════════════════════════════════════════════════════
#  Makefile
#  Все цели сгруппированы по смыслу. Запуск: make <target>
# ═══════════════════════════════════════════════════════════════════

# Не интерпретировать цели как файлы
.PHONY: help \
        env \
        up down restart logs ps \
        build build-no-cache \
        fastapi-shell django-shell postgres-shell \
        migrate-fastapi migrate-django migrate \
        migrations-fastapi makemigrations-django \
        test test-fastapi test-django test-cov \
        lint lint-fastapi lint-django fmt fmt-fastapi fmt-django \
        pre-commit-install pre-commit-run \
        clean clean-volumes clean-all \
        prod-build prod-up prod-down \
        topics kafka-topics

# Переменные
DC          = docker compose
DC_TEST     = docker compose -f docker-compose.yml -f docker-compose.test.yml
FASTAPI_CTR = $(shell $(DC) ps -q fastapi 2>/dev/null)
DJANGO_CTR  = $(shell $(DC) ps -q django 2>/dev/null)

# ─────────────────────────────────────────────────────────────────
# HELP  (цель по умолчанию)
# ─────────────────────────────────────────────────────────────────

help: ## Показать это сообщение
	@echo ""
	@echo "  \033[1mДоступные команды:\033[0m"
	@echo ""
	@awk 'BEGIN {FS = ":.*##"} /^[a-zA-Z_-]+:.*##/ \
		{ printf "  \033[36m%-26s\033[0m %s\n", $$1, $$2 }' $(MAKEFILE_LIST)
	@echo ""

# ─────────────────────────────────────────────────────────────────
# SETUP
# ─────────────────────────────────────────────────────────────────

env: ## Создать .env из .env.example (если .env не существует)
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
		echo "  \033[32m✔\033[0m .env создан из .env.example. Заполни секреты!"; \
	else \
		echo "  \033[33m!\033[0m .env уже существует, пропускаем."; \
	fi

# ─────────────────────────────────────────────────────────────────
# DOCKER — основные операции
# ─────────────────────────────────────────────────────────────────

up: ## Поднять все сервисы в фоне
	$(DC) up -d

down: ## Остановить все сервисы
	$(DC) down

restart: ## Перезапустить все сервисы
	$(DC) restart

logs: ## Следить за логами (все сервисы). Пример: make logs s=fastapi
	$(DC) logs -f $(s)

ps: ## Статус контейнеров
	$(DC) ps

build: ## Собрать образы
	$(DC) build

build-no-cache: ## Собрать образы без кэша
	$(DC) build --no-cache

# ─────────────────────────────────────────────────────────────────
# SHELLS
# ─────────────────────────────────────────────────────────────────

fastapi-shell: ## Открыть bash внутри контейнера fastapi
	$(DC) exec fastapi bash

django-shell: ## Открыть Django shell
	$(DC) exec django python manage.py shell

postgres-shell: ## Открыть psql
	$(DC) exec postgres psql -U $${POSTGRES_USER} -d $${POSTGRES_DB}

redis-shell: ## Открыть redis-cli
	$(DC) exec redis redis-cli -a $${REDIS_PASSWORD}

# ─────────────────────────────────────────────────────────────────
# MIGRATIONS
# ─────────────────────────────────────────────────────────────────

migrate-fastapi: ## Применить Alembic миграции
	$(DC) exec fastapi alembic upgrade head

migrate-django: ## Применить Django миграции
	$(DC) exec django python manage.py migrate

migrate: migrate-fastapi migrate-django ## Применить все миграции

migrations-fastapi: ## Создать Alembic миграцию. Пример: make migrations-fastapi m="add users table"
	$(DC) exec fastapi alembic revision --autogenerate -m "$(m)"

makemigrations-django: ## Создать Django миграции. Пример: make makemigrations-django app=users
	$(DC) exec django python manage.py makemigrations $(app)

migration-history: ## История Alembic миграций
	$(DC) exec fastapi alembic history --verbose

migration-current: ## Текущая Alembic ревизия
	$(DC) exec fastapi alembic current

migration-downgrade: ## Откатить последнюю Alembic миграцию
	$(DC) exec fastapi alembic downgrade -1

# ─────────────────────────────────────────────────────────────────
# TESTS
# ─────────────────────────────────────────────────────────────────

test-fastapi: ## Запустить тесты FastAPI
	$(DC_TEST) run --rm fastapi

test-django: ## Запустить тесты Django
	$(DC_TEST) run --rm django

test: test-fastapi test-django ## Запустить все тесты

test-cov: ## Тесты с отчётом о покрытии (HTML)
	$(DC) run --rm \
		-e COVERAGE_FILE=/app/.coverage \
		fastapi \
		pytest tests/ -v --asyncio-mode=auto \
		       --cov=app --cov-report=html:/app/htmlcov --cov-report=term-missing
	@echo "  \033[32m✔\033[0m Coverage report: fastapi_service/htmlcov/index.html"
	$(DC) run --rm \
		django \
		pytest tests/ -v \
		       --cov=apps --cov-report=html:/app/htmlcov --cov-report=term-missing
	@echo "  \033[32m✔\033[0m Coverage report: django_service/htmlcov/index.html"

test-file: ## Запустить конкретный файл тестов. Пример: make test-file svc=fastapi f=tests/test_auth.py
	$(DC) run --rm $(svc) pytest $(f) -v --asyncio-mode=auto

# ─────────────────────────────────────────────────────────────────
# LINTING & FORMATTING
# ─────────────────────────────────────────────────────────────────

lint-fastapi: ## Линтинг FastAPI (ruff + mypy)
	$(DC) run --rm fastapi sh -c "ruff check app/ && mypy app/"

lint-django: ## Линтинг Django (ruff + mypy)
	$(DC) run --rm django sh -c "ruff check apps/ config/ && mypy apps/ config/"

lint: lint-fastapi lint-django ## Линтинг всего проекта

fmt-fastapi: ## Форматирование FastAPI (ruff format)
	$(DC) run --rm fastapi ruff format app/ tests/

fmt-django: ## Форматирование Django (ruff format)
	$(DC) run --rm django ruff format apps/ config/ tests/

fmt: fmt-fastapi fmt-django ## Форматирование всего проекта

# ─────────────────────────────────────────────────────────────────
# PRE-COMMIT
# ─────────────────────────────────────────────────────────────────

pre-commit-install: ## Установить pre-commit хуки локально
	pip install pre-commit
	pre-commit install
	pre-commit install --hook-type commit-msg
	@echo "  \033[32m✔\033[0m pre-commit хуки установлены"

pre-commit-run: ## Запустить все pre-commit хуки на всех файлах
	pre-commit run --all-files

# ─────────────────────────────────────────────────────────────────
# KAFKA / REDPANDA
# ─────────────────────────────────────────────────────────────────

topics: ## Создать все Kafka-топики через rpk
	@echo "  Создаю топики..."
	$(DC) exec redpanda rpk topic create jobs.created          --partitions 8 --replicas 1
	$(DC) exec redpanda rpk topic create jobs.completed        --partitions 8 --replicas 1
	$(DC) exec redpanda rpk topic create jobs.failed           --partitions 4 --replicas 1
	$(DC) exec redpanda rpk topic create batches.progress      --partitions 4 --replicas 1
	@echo "  \033[32m✔\033[0m Топики созданы"

kafka-topics: ## Список всех топиков
	$(DC) exec redpanda rpk topic list

kafka-consume: ## Читать топик в реальном времени. Пример: make kafka-consume t=jobs.created
	$(DC) exec redpanda rpk topic consume $(t) --brokers=localhost:9092

# ─────────────────────────────────────────────────────────────────
# CLEANUP
# ─────────────────────────────────────────────────────────────────

clean: ## Остановить контейнеры и удалить образы проекта
	$(DC) down --rmi local

clean-volumes: ## Остановить контейнеры и удалить volumes (ОСТОРОЖНО: данные БД!)
	$(DC) down -v
	@echo "  \033[31m!\033[0m Volumes удалены."

clean-all: ## Полная очистка: контейнеры + образы + volumes + кэш сборки
	$(DC) down -v --rmi all --remove-orphans
	docker builder prune -f
	@echo "  \033[31m!\033[0m Всё удалено."

clean-pyc: ## Удалить .pyc и __pycache__
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache"   -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache"   -exec rm -rf {} + 2>/dev/null || true
	@echo "  \033[32m✔\033[0m Python cache очищен"

# ─────────────────────────────────────────────────────────────────
# PRODUCTION (отдельный target-набор)
# ─────────────────────────────────────────────────────────────────

prod-build: ## Собрать production-образы
	$(DC) -f docker-compose.yml -f docker-compose.prod.yml build

prod-up: ## Поднять в production-режиме
	$(DC) -f docker-compose.yml -f docker-compose.prod.yml up -d

prod-down: ## Остановить production
	$(DC) -f docker-compose.yml -f docker-compose.prod.yml down
