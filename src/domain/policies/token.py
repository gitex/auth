from src.domain.policies import Policy
from src.domain.types import PotentialIssues
from src.domain.value_objects import Claims, Issue, IssueCode, IssueSeverity


class SubRequiredPolicy(Policy[Claims]):
    """Token should contain 'sub' claim."""

    def evaluate(self, ctx: Claims) -> PotentialIssues:
        if ctx.sub is None:
            yield Issue(
                code=IssueCode.REQUIRED_SUB,
                severity=IssueSeverity.HIGH,
                ctx={'sub': ctx.sub},
            )


class JtiRequiredPolicy(Policy[Claims]):
    """Token should contain 'jti' claim."""

    def evaluate(self, ctx: Claims) -> PotentialIssues:
        if ctx.jti is None:
            yield Issue(
                code=IssueCode.REQUIRED_JTI,
                severity=IssueSeverity.HIGH,
                ctx={'jti': ctx.jti},
            )


class ExpRequiredPolicy(Policy[Claims]):
    """Token should contain 'exp' claim."""

    def evaluate(self, ctx: Claims) -> PotentialIssues:
        if ctx.exp is None:
            yield Issue(
                code=IssueCode.REQUIRED_EXP,
                severity=IssueSeverity.HIGH,
                ctx={'exp': ctx.exp},
            )


class NotExpiredPolicy(Policy[Claims]):
    """Token should not be expired."""

    def __init__(self, now: int, skew: int = 0) -> None:
        self.now = now
        self.skew = skew

    def evaluate(self, ctx: Claims) -> PotentialIssues:
        if ctx.exp is None:
            yield Issue(
                code=IssueCode.REQUIRED_EXP,
                severity=IssueSeverity.HIGH,
                ctx={'exp': ctx.exp},
            )

        elif (ctx.exp + self.skew) < self.now:
            yield Issue(
                code=IssueCode.EXPIRED,
                severity=IssueSeverity.HIGH,
                ctx={'now': self.now, 'exp': ctx.exp, 'skew': self.skew},
            )
