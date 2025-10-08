from typing import Protocol, TypeVar, runtime_checkable

from src.domain.types import PotentialIssues
from src.domain.value_objects import Decision, Issue


Ctx = TypeVar('Ctx')


@runtime_checkable
class Policy[Ctx](Protocol):
    """Policy of business operation.

    Usage:

    class TokenNotExpired(Policy[Claims]):
        error_message: ClassVar[str] = 'Token expired'

        def decide(self, value: Claims) -> Decision:
            ... # calculate decision
            ... # decided 'no'
            return Decision.from_error_message(self.error_message)
            ... # or decided 'yes'
            return Decision.success()
    """

    def evaluate(self, ctx: Ctx) -> PotentialIssues: ...


class PolicySuite(Policy[Ctx]):
    """Suite of policies.

    Usage:

    suite = PolicySuite(
        SubRequired(),
        ExpRequired(),
        Expiration(now=now)
        ...
    )
    suite.decide(claims)
    """

    def __init__(self, *policies: Policy) -> None:
        self._policies = policies

    def decide(self, ctx: Ctx) -> Decision:
        issues: list[Issue] = []

        for policy in self._policies:
            for issue in policy.evaluate(ctx):
                if not issue:
                    continue
                issues.append(issue)

        return Decision(issues)
