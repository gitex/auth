"""Tests for Specification pattern."""

from uuid import uuid4

from src.domain.entities import Account
from src.domain.specifications import Specification
from src.domain.value_objects import Email, PasswordHash


class ActiveAccountSpec(Specification[Account]):
    """Specification for active accounts."""

    def is_satisfied_by(self, candidate: Account) -> bool:
        """Check if account is active."""
        return candidate.is_active


class EmailDomainSpec(Specification[Account]):
    """Specification for accounts with specific email domain."""

    def __init__(self, domain: str) -> None:
        self.domain = domain

    def is_satisfied_by(self, candidate: Account) -> bool:
        """Check if account email matches domain."""
        return candidate.email.value.endswith(f'@{self.domain}')


class TestSpecification:
    """Tests for Specification pattern."""

    def test_specification_is_satisfied_by(self) -> None:
        """Test basic specification satisfaction."""
        spec = ActiveAccountSpec()
        account = Account(
            identifier=uuid4(),
            email=Email('test@example.com'),
            password_hash=PasswordHash('hash'),
            is_active=True,
        )

        assert spec.is_satisfied_by(account) is True

    def test_specification_is_not_satisfied(self) -> None:
        """Test specification not satisfied."""
        spec = ActiveAccountSpec()
        account = Account(
            identifier=uuid4(),
            email=Email('test@example.com'),
            password_hash=PasswordHash('hash'),
            is_active=False,
        )

        assert spec.is_satisfied_by(account) is False

    def test_and_specification_both_satisfied(self) -> None:
        """Test AND specification when both are satisfied."""
        spec1 = ActiveAccountSpec()
        spec2 = EmailDomainSpec('example.com')
        combined = spec1.and_(spec2)

        account = Account(
            identifier=uuid4(),
            email=Email('test@example.com'),
            password_hash=PasswordHash('hash'),
            is_active=True,
        )

        assert combined.is_satisfied_by(account) is True

    def test_and_specification_one_not_satisfied(self) -> None:
        """Test AND specification when one is not satisfied."""
        spec1 = ActiveAccountSpec()
        spec2 = EmailDomainSpec('example.com')
        combined = spec1.and_(spec2)

        account = Account(
            identifier=uuid4(),
            email=Email('test@other.com'),
            password_hash=PasswordHash('hash'),
            is_active=True,
        )

        assert combined.is_satisfied_by(account) is False

    def test_or_specification_one_satisfied(self) -> None:
        """Test OR specification when one is satisfied."""
        spec1 = ActiveAccountSpec()
        spec2 = EmailDomainSpec('example.com')
        combined = spec1.or_(spec2)

        account = Account(
            identifier=uuid4(),
            email=Email('test@other.com'),
            password_hash=PasswordHash('hash'),
            is_active=True,
        )

        assert combined.is_satisfied_by(account) is True

    def test_or_specification_both_satisfied(self) -> None:
        """Test OR specification when both are satisfied."""
        spec1 = ActiveAccountSpec()
        spec2 = EmailDomainSpec('example.com')
        combined = spec1.or_(spec2)

        account = Account(
            identifier=uuid4(),
            email=Email('test@example.com'),
            password_hash=PasswordHash('hash'),
            is_active=True,
        )

        assert combined.is_satisfied_by(account) is True

    def test_or_specification_none_satisfied(self) -> None:
        """Test OR specification when none are satisfied."""
        spec1 = ActiveAccountSpec()
        spec2 = EmailDomainSpec('example.com')
        combined = spec1.or_(spec2)

        account = Account(
            identifier=uuid4(),
            email=Email('test@other.com'),
            password_hash=PasswordHash('hash'),
            is_active=False,
        )

        assert combined.is_satisfied_by(account) is False

    def test_not_specification_negates(self) -> None:
        """Test NOT specification negates the result."""
        spec = ActiveAccountSpec()
        negated = spec.not_()

        active_account = Account(
            identifier=uuid4(),
            email=Email('test@example.com'),
            password_hash=PasswordHash('hash'),
            is_active=True,
        )

        inactive_account = Account(
            identifier=uuid4(),
            email=Email('test@example.com'),
            password_hash=PasswordHash('hash'),
            is_active=False,
        )

        assert negated.is_satisfied_by(active_account) is False
        assert negated.is_satisfied_by(inactive_account) is True

    def test_complex_specification_composition(self) -> None:
        """Test complex specification with multiple operators."""
        # (Active AND example.com) OR gmail.com
        spec = ActiveAccountSpec().and_(EmailDomainSpec('example.com')).or_(
            EmailDomainSpec('gmail.com')
        )

        # Should match: active + example.com
        account1 = Account(
            identifier=uuid4(),
            email=Email('test@example.com'),
            password_hash=PasswordHash('hash'),
            is_active=True,
        )
        assert spec.is_satisfied_by(account1) is True

        # Should match: any status + gmail.com
        account2 = Account(
            identifier=uuid4(),
            email=Email('test@gmail.com'),
            password_hash=PasswordHash('hash'),
            is_active=False,
        )
        assert spec.is_satisfied_by(account2) is True

        # Should not match: inactive + example.com
        account3 = Account(
            identifier=uuid4(),
            email=Email('test@example.com'),
            password_hash=PasswordHash('hash'),
            is_active=False,
        )
        assert spec.is_satisfied_by(account3) is False
