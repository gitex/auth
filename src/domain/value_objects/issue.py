from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any


class IssueSeverity(StrEnum):
    HIGH = 'high'
    MEDIUM = 'medium'
    LOW = 'low'


class IssueCode(StrEnum):
    REQUIRED_SUB = 'token:required:sub'
    REQUIRED_JTI = 'token:required:jti'
    REQUIRED_EXP = 'token:required:exp'
    EXPIRED = 'token:expired'


@dataclass(frozen=True, slots=True)
class Issue:
    code: IssueCode
    severity: IssueSeverity = IssueSeverity.HIGH
    ctx: dict[str, Any] | None = None

    def is_critical(self) -> bool:
        return self.severity is IssueSeverity.HIGH


@dataclass(frozen=True, slots=True)
class Decision:
    issues: list[Issue] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return any(issue for issue in self.issues if issue.is_critical())

    @classmethod
    def from_issues(cls, issues: list[Issue]) -> 'Decision':
        return cls(issues)
