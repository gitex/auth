from typing import Any


class URL(str):  # noqa: FURB189, SLOT000
    """URL builder.

    Usage:
        >> api = URL('api/v1')
        >> users = api / 'users'
        >> users == 'api/v1/users'
        True
        >> user = users / "{id}"
        >> user.path(id=2)
        api/v1/users/2
    """

    def path(self, **params: Any) -> 'URL':  # noqa: ANN401
        """Put id into URL."""
        return URL(self.format(**params))

    def __truediv__(self, right: str) -> 'URL':
        """Division as way to join segments."""
        if not self or self == '/':
            return URL(f'/{right}')
        return URL(f'{self}/{right}')


# API = URL('/api/v1')  # noqa: ERA001 Add prefix to application
API = URL('')


class URLS:
    """URLs for testing with client.

    Single point of truth for URLs.
    """

    login: URL = API / 'login'
    register: str = API / 'register'
    me: URL = API / 'me'
