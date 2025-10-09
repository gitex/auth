# API

## 'POST /register'

Request:
```json
{"email": "a@b.c", "password": "pass"}
```

Response:
```json
{ "user_id": "1", "requires_verification": true}
```

## `POST /login`

Request:
```json
{"email": "a@b.c", "password": "pass"}
```

Response:
```json
{
    "access_token": "...",
    "refresh_token": "...",
    "token_type": "Bearer",
}
```

## `POST /refresh`

Request:
```json
{"refrsh": "..."}
```

Request:
```json
{
    "access_token": "...",
    "refresh_token": "...",
    "token_type": "Bearer",
}
```

## `POST /forgot-password`

Request:
```json
{"email": "a@b.c"}
```

## `POST /reset-password`

Request:
```json
{"token": "...", "new_pasword": "..."}
```

## `GET /me` + Token

Response
```json
{
    "id": "1",
    "email": "a@b.c",
    "username": "abc",
    "roles": ["user"],
    "is_verified": true,
}
```

## `POST /change-password` + Token

Request:
```json
{"old_password": "...", "new_password": "..."}
```

Response: 204, 400, 401

## `GET /sessions` + Token

Response:
```json
[
    {"family_id": "family_1", "device": "Chrome Lunix", "created_at": "", "last_used_at", ...},
    ...
]
```

## `POST /logout` + Token

Помечаем текущий refresh как revoked, access истечёт сам

## `POST /sessions/{family_id}/revoke`

## `POST /logout/all`

## `POST /introspect`

Request:
```json
{
    "token": "...",
}
```

Response:
```json
{
    "is_active": true,

    "sub": "user_id",
    "scope": "...",
    "exp": 1838832772,
    "type": "access",
}
{
    "is_active": false,
}
```

## `GET /healthz` -> 200





