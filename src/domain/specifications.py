"""Specification pattern for composable business rules and queries.

The Specification pattern allows building complex business rules by composing
simple specifications using logical operators (AND, OR, NOT).
"""

from abc import abstractmethod
from typing import Protocol, TypeVar


T = TypeVar('T')


class Specification(Protocol[T]):
    """Base specification interface.
    
    A specification encapsulates a business rule that can be checked
    against a candidate object. Specifications can be combined using
    logical operators to create complex rules.
    """

    @abstractmethod
    def is_satisfied_by(self, candidate: T) -> bool:
        """Check if candidate satisfies this specification.
        
        Args:
            candidate: Object to check against specification
            
        Returns:
            True if candidate satisfies specification, False otherwise
        """
        ...

    def and_(self, other: 'Specification[T]') -> 'Specification[T]':
        """Combine specifications with logical AND.
        
        Args:
            other: Specification to combine with
            
        Returns:
            New specification that is satisfied only if both are satisfied
        """
        return AndSpecification(self, other)

    def or_(self, other: 'Specification[T]') -> 'Specification[T]':
        """Combine specifications with logical OR.
        
        Args:
            other: Specification to combine with
            
        Returns:
            New specification that is satisfied if either is satisfied
        """
        return OrSpecification(self, other)

    def not_(self) -> 'Specification[T]':
        """Negate this specification.
        
        Returns:
            New specification that is satisfied if this is not satisfied
        """
        return NotSpecification(self)


class AndSpecification(Specification[T]):
    """Specification combining two specifications with AND logic."""

    def __init__(self, left: Specification[T], right: Specification[T]) -> None:
        self.left = left
        self.right = right

    def is_satisfied_by(self, candidate: T) -> bool:
        """Check if candidate satisfies both specifications."""
        return self.left.is_satisfied_by(candidate) and self.right.is_satisfied_by(
            candidate
        )


class OrSpecification(Specification[T]):
    """Specification combining two specifications with OR logic."""

    def __init__(self, left: Specification[T], right: Specification[T]) -> None:
        self.left = left
        self.right = right

    def is_satisfied_by(self, candidate: T) -> bool:
        """Check if candidate satisfies either specification."""
        return self.left.is_satisfied_by(candidate) or self.right.is_satisfied_by(
            candidate
        )


class NotSpecification(Specification[T]):
    """Specification that negates another specification."""

    def __init__(self, spec: Specification[T]) -> None:
        self.spec = spec

    def is_satisfied_by(self, candidate: T) -> bool:
        """Check if candidate does not satisfy the specification."""
        return not self.spec.is_satisfied_by(candidate)
