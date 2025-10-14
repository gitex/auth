from collections import defaultdict
from collections.abc import Callable
from typing import Any, Protocol, TypeVar, final, override

from src.domain.events import DomainEvent
from src.domain.ports import DomainEventPublisher

from src.infra.dto import OutboxDto
from src.infra.repositories.outbox import OutboxRepository


class KafkaEventPublisher(Protocol):
    topic: str = NotImplemented
    event_type: str = NotImplemented
    version: str = '1'

    @property
    def headers(self) -> dict[str, Any]:
        return {'type': self.event_type, 'v': self.version}


K = TypeVar('K')
V = TypeVar('V')


@final
class ClassRegistry[K, V]:
    __slots__: tuple[str] = ('_storage',)

    def __init__(self) -> None:
        self._storage: dict[type[K], list[type[V]]] = defaultdict(list)

    def add(self, key: type[K], value: type[V]) -> None:
        self._storage[key].append(value)

    def get(
        self, key: type[K], default: list[type[V]] | None = None
    ) -> list[type[V]] | None:
        return self._storage.get(key, default)

    def register(self, key: type[K]) -> Callable[..., type[V]]:
        def wrapper(cls: type[V]) -> type[V]:
            self.add(key, cls)
            return cls

        return wrapper


event_publisher = ClassRegistry[DomainEvent, KafkaEventPublisher]()


@event_publisher.register(DomainEvent)
class UserRegisteredPublisher(KafkaEventPublisher):
    topic: str = 'acccount.registered'
    event_type: str = 'AccountRegistered'
    version: str = '1'


@final
class OutboxEventPublisher(DomainEventPublisher):
    def __init__(self, outbox_repository: OutboxRepository) -> None:
        self._repo = outbox_repository

    @override
    async def publish(self, event: DomainEvent) -> None:
        publishers = event_publisher.get(event.__class__)
        if not publishers:
            return

        for publisher_class in publishers:
            publisher = publisher_class()

            outbox_dto = OutboxDto(
                topic=publisher.topic,
                headers=publisher.headers,
                payload=event.as_dict(),
            )

            await self._repo.create(outbox_dto)
