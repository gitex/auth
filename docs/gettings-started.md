### Запуск сервиса

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


