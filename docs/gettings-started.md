# Начало работы с сервисом

## Запуск сервиса

Для удобной работы с сервисом рекомендуется [установить just](https://github.com/casey/just?tab=readme-ov-file#packages).

Сервис запускается из корня репозитория командами
```bash
# Создаём побочные файлы (.env), инициализируем pre-commit
just init

# Запускаем зависимости (redis, database, kafka)
just up

# Запускаем сервис
just up service
```

## Команды

### just init

Цель: быстрая и удобная развертка проекта

Действия:
- Создаёт файл `.env` из [env.example](../env.example), если файл не был создан ранее.
- Инициализирует `pre-commit` с репозиторием.

### just up

Цель: быстро поднимать контейнеры через profiles.

Действия:

- **just up <profile>**: запускает docker compose по profile. По умолчанию - `profile=dependencies`
- **just up dependencies**: запускает зависимости проекта (database, kafka, redis)
- **just up service**: запускает микросервис в Docker

### just down

Цель: быстро ронять контейнеры через profiles.

Действия:

- **just down**: останавливает docker compose по profile. По умолчанию - `profile=dependencies`
- **just down dependencies**: останавливает зависимости проекта (database, kafka, redis)
- **just down service**: останавливает микросервис в Docker

### just ps

alias для `sudo docker compose ps`

### just logs <target>

alias для `sudo docker logs -f <target>`
