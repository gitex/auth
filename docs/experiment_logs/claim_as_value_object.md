# Эксперимент: использовать Claims с value objects (DDD)

## Гипотеза
Это улучшит читаемость и работу между объектами

## Контекст

```python
@dataclass(frozen=True, slots=True)
class Instant:
    dt: datetime

...

Claims:
    aud: Audience
    sub: Sub
    exp: Instant
    iat: Instant
```

## Наблюдения

## Исход

Усложнились даже самые простые сборки. Если `Instant + Duration` удалось подружить,
то, например `ClockSkew` казался избыточным.

Глобальная проблема возникла в превращении Claims в сам токен: json не переварил кучу объектов
и пришлось продумывать маппинг

```python
def claims_to_payload(claims: Claims) -> dict[str, Any]:
    payload: dict[str, Any] = {}

    if claims.sub is not None:
        payload['sub'] = claims.sub

    if claims.iss is not None:
        payload['iss'] = claims.iss.value

    if claims.jti is not None:
        payload['jti'] = claims.jti.value

    if claims.aud is not None:
        auds = sorted(claims.aud.values)

        if not auds:
            pass
        elif len(auds) == 1:
            payload['aud'] = auds[0]
        else:
            payload['aud'] = auds

    if claims.exp is not None:
        payload['exp'] = claims.exp.as_epoch()

    if claims.nbf is not None:
        payload['nbf'] = claims.nbf.as_epoch()

    if claims.iat is not None:
        payload['iat'] = claims.iat.as_epoch()

    # Private
    if claims.email is not None:
        payload['email'] = claims.email.value

    return payload
```

Разумеется, возможен и обратный маппинг. Как результат - при добавлении нового claim -
код нужно менять в трех местах.

## Решение

Отказался от VO в claims, перешёл на примитивы. Возможно дело конкретно в JWT, но
выглядит больновато и сложно.
