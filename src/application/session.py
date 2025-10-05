from uow import SqlAlchemyUoW

from infra.config import settings
from src.infra.orm.session import (
    make_async_session_factory,
    make_engine,
)


engine = make_engine(
    url=settings.database_url,
    echo=settings.debug,
)
SessionFactory = make_async_session_factory(engine)
uow = SqlAlchemyUoW(SessionFactory)
