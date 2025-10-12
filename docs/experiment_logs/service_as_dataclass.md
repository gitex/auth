# Эксперимент: использовать инициализацию сервиса через dataclass

## Гипотеза

Красиво и практично. Внутри без `._dependency`, а с `frozen=True` еще и не изменяемые

## Контекст

```python
@dataclass(frozen=True, slots=True)
class SomeService:
    dep1: Dep1
    dep2: Dep2


class SomeService(dep1=..., dep2=...)
```

## Наблюдения

В целом все работает хорошо, но методы начинают "высвечивать" наружу:


```python
class Service(Protocol):
    def do_thing(self) -> int: ...
    def do_other_thing(self) -> str: ...
```

Согласно протоколу есть некий `Service` с методами `do_thing()` и `do_other_thing`.

Создаем сервис по протоколу:

```python
@dataclass
class ServiceImpl(Service):
    builder: Builder
    config: Config

    def do_thing(self) -> int:
        return builder.incr(config.default).build()

    def do_other_thing(self) -> str:
        return builder.incr(config.default).as_str().build()
```

По протоколу реализовали методы `do_thing()` и `do_other_thing()`,
но `builder` и `config` теперь так же доступны из сервиса.

Особенно это опасно, если соседнему сервису понадобится `config`, который вот тут рядышком
в `ServiceImpl`. Появляется соблазн его забрать.

```python
class ApplicationService:
    neighboor: OtherNeighborService
    service: ServiceImpl  # <- наш сервис

    def method(self):
        value = self.service.do_thing()

        # тут лезем в конфиг, которого в нет в Protocol
        neighboor.get(self.service.config.redis_key)
```

Но `ServiceImpl` меняется (по протоколу - инициализация не описана, а значит может менять как угодно),
вместо `config` появляется `provider` и соседний сервис отваливается.

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
