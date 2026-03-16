-- Инициализация выполняется один раз при первом запуске postgres-контейнера.
-- Расширения, которые нужны приложению.

CREATE EXTENSION IF NOT EXISTS "pgcrypto";   -- gen_random_uuid()
CREATE EXTENSION IF NOT EXISTS "pg_trgm";    -- trigram-индексы для поиска по тексту
CREATE EXTENSION IF NOT EXISTS "btree_gin";  -- GIN-индексы на скалярах
