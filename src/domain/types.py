from collections.abc import Iterable

from src.domain.value_objects import Issue


type PotentialIssues = Iterable[Issue]
