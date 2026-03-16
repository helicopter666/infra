# Project Name

> Краткое описание проекта.

## Стек

| Слой | Технология |
|---|---|
| FastAPI Service | Python 3.12, FastAPI, SQLAlchemy 2, Alembic |
| Django Service | Python 3.12, Django 5, DRF |
| База данных | PostgreSQL 16 |
| Очередь | Redpanda (Kafka-совместимый) + FastStream |
| Кэш / Blacklist | Redis 7 |
| LLM | OpenRouter API |

---

## Быстрый старт

### 1. Клонировать репозиторий

```bash
git clone <repo-url>
cd <project>
```

### 2. Подготовить окружение

```bash
make env          # создаст .env из .env.example
# отредактировать .env: вставить OPENROUTER_API_KEY, сменить пароли
```

### 3. Установить pre-commit хуки

```bash
make pre-commit-install
```

### 4. Поднять сервисы

```bash
make up           # docker compose up -d
make migrate      # alembic upgrade head + django migrate
make topics       # создать Kafka-топики в Redpanda
```

### 5. Проверить

```
FastAPI:           http://localhost:8000/docs
Django Admin:      http://localhost:8001/admin
Redpanda Console:  http://localhost:8080
```

---

## Команды

| Команда | Описание |
|---|---|
| `make up` | Поднять все сервисы |
| `make down` | Остановить |
| `make logs s=fastapi` | Логи конкретного сервиса |
| `make migrate` | Применить все миграции |
| `make migrations-fastapi m="описание"` | Создать Alembic-миграцию |
| `make test` | Запустить все тесты |
| `make test-cov` | Тесты + HTML-отчёт о покрытии |
| `make lint` | Линтинг (ruff + mypy) |
| `make fmt` | Форматирование (ruff format) |
| `make topics` | Создать Kafka-топики |
| `make clean-volumes` | ⚠️ Удалить все данные (volumes) |

Полный список: `make help`

---

## Структура проекта

```
.
├── fastapi_service/           # Core API (FastAPI)
│   ├── app/
│   │   ├── api/v1/            # Эндпоинты
│   │   ├── core/              # Конфиг, JWT, зависимости
│   │   ├── db/                # SQLAlchemy модели, сессия
│   │   ├── schemas/           # Pydantic request/response
│   │   ├── services/          # Бизнес-логика, LLM-клиент
│   │   ├── messaging/         # FastStream broker + consumers
│   │   └── cache/             # Redis утилиты
│   ├── alembic/               # Миграции
│   ├── tests/
│   ├── Dockerfile
│   ├── alembic.ini
│   ├── pyproject.toml
│   └── requirements.txt
│
├── django_service/            # Admin & Analytics (Django)
│   ├── apps/
│   │   ├── users/
│   │   └── analytics/
│   ├── config/
│   │   ├── settings/
│   │   │   ├── base.py
│   │   │   ├── local.py
│   │   │   └── test.py
│   │   └── urls.py
│   ├── tests/
│   ├── Dockerfile
│   ├── pyproject.toml
│   └── requirements.txt
│
├── scripts/
│   ├── init-db.sql            # PostgreSQL расширения
│   └── redpanda-console-config.yaml
│
├── docker-compose.yml
├── docker-compose.test.yml
├── Makefile
├── .env.example
├── .gitignore
├── .pre-commit-config.yaml
└── .commitlintrc.yaml
```

---

## Переменные окружения

Все переменные описаны в `.env.example`. Обязательные для заполнения:

| Переменная | Описание |
|---|---|
| `OPENROUTER_API_KEY` | API-ключ OpenRouter |
| `JWT_SECRET_KEY` | Секрет для JWT (минимум 32 символа) |
| `POSTGRES_PASSWORD` | Пароль PostgreSQL |
| `REDIS_PASSWORD` | Пароль Redis |
| `DJANGO_SECRET_KEY` | Django SECRET_KEY |

Генерация безопасных секретов:
```bash
openssl rand -hex 32
```

---

## Тесты

```bash
make test                                         # все тесты
make test-fastapi                                 # только FastAPI
make test-django                                  # только Django
make test-file svc=fastapi f=tests/test_auth.py  # один файл
make test-cov                                     # с HTML coverage-отчётом
```

Минимальный coverage: FastAPI ≥ 80%, Django ≥ 70%.

---

## Conventional Commits

Проект использует [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add batch job endpoint
fix: correct JWT expiry calculation
docs: update README quickstart
refactor(llm): extract prompt builder to separate module
test: add integration tests for extraction worker
chore: bump fastapi to 0.115.0
```

Формат проверяется автоматически через pre-commit хук `commitizen`.
