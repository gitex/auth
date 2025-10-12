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
- **just up deps**: запускает зависимости проекта (database, kafka, redis)
- **just up service**: запускает микросервис в Docker

### just down

Цель: быстро ронять контейнеры через profiles.

Действия:

- **just down**: останавливает docker compose по profile. По умолчанию - `profile=dependencies`
- **just down deps**: останавливает зависимости проекта (database, kafka, redis)
- **just down service**: останавливает микросервис в Docker

### just ps

alias для `sudo docker compose ps`

### just logs <target>

alias для `sudo docker logs -f <target>`


## Tmux

В проекте есть запуск через tmux, который автоматизирует развертку еще больше:
```bash
just dev
```
- Запускает `deps` (зависимости)
- Запускает [`tmux`](../.tmuxp.yml) с 4 вкладками (windows)
- После работы - оставливает зависимости и сам сервис

## FAQ

#### Q: Запускаю justfile, но Docker требует sudo

**A:** https://docs.docker.com/engine/install/linux-postinstall/

```bash
sudo groupadd docker
sudo usermod -aG docker $USER
newgrp docker
```
