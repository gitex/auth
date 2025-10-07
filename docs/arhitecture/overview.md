### Domain

Доменная область в *Auth* отвечает за безопасность. Наличие логики jwt внутри домена не поощряется.

#### Entities

- **Identity** / **Account**: id, email, is_active и прочее
- **Credential**. Пароль/ключ
- **Session / RefreshSession**. TTL, цепочки, rotation, revoked_at
- **Key**. Подпись токенов (kid/ротация ключей)
- **AuditEvent**. Факт логина/логаута/смены пароля/блокировки

#### Value-objects

- Email
- PasswordHash
- Scope
- Role
- Permission
- IpAddress
- UserAgent

#### Services

- **PasswordPolicy**. Требования к паролю: длина, состав,
история (не переиспользовать), срок жизни и прочее.
- **LockoutPolicy**. Блокируем на время, если N раз неуспешных попыток.
- **TokenPolicy**. Что содержит, TTL, audience/issuer

#### События

- **user.registered**
- **user.loggedin**
- **password.changed**
- **user.locked**
- **refresh.rotated**


