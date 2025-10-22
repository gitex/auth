"""Result pattern for functional error handling.

This module implements the Result pattern which allows handling errors
in a functional way without using exceptions for control flow.
"""

from dataclasses import dataclass
from typing import Callable, Generic, TypeVar


T = TypeVar('T')
E = TypeVar('E')
U = TypeVar('U')


@dataclass(frozen=True)
class Result(Generic[T, E]):
    """Base Result type for functional error handling.
    
    Result represents an operation that can either succeed with a value
    or fail with an error. This is a sealed type with two variants:
    Success and Failure.
    """

    def is_success(self) -> bool:
        """Check if result is Success."""
        return isinstance(self, Success)

    def is_failure(self) -> bool:
        """Check if result is Failure."""
        return isinstance(self, Failure)

    def unwrap(self) -> T:
        """Get value or raise if Failure.
        
        Raises:
            ValueError: If result is Failure
        """
        if isinstance(self, Success):
            return self.value
        msg = f'Called unwrap on Failure: {self.error}'
        raise ValueError(msg)

    def unwrap_or(self, default: T) -> T:
        """Get value or return default if Failure."""
        if isinstance(self, Success):
            return self.value
        return default

    def map(self, f: Callable[[T], U]) -> 'Result[U, E]':
        """Transform the success value using function f.
        
        If Result is Success, applies f to value and returns Success(f(value)).
        If Result is Failure, returns Failure unchanged.
        """
        if isinstance(self, Success):
            return Success(f(self.value))
        return self  # type: ignore[return-value]

    def map_error(self, f: Callable[[E], U]) -> 'Result[T, U]':
        """Transform the error value using function f.
        
        If Result is Failure, applies f to error and returns Failure(f(error)).
        If Result is Success, returns Success unchanged.
        """
        if isinstance(self, Failure):
            return Failure(f(self.error))
        return self  # type: ignore[return-value]

    def and_then(self, f: Callable[[T], 'Result[U, E]']) -> 'Result[U, E]':
        """Chain operations that return Result.
        
        If Result is Success, applies f to value and returns its Result.
        If Result is Failure, returns Failure unchanged.
        This is also known as flatMap or bind in functional programming.
        """
        if isinstance(self, Success):
            return f(self.value)
        return self  # type: ignore[return-value]


@dataclass(frozen=True)
class Success(Result[T, E]):
    """Successful result containing a value."""

    value: T


@dataclass(frozen=True)
class Failure(Result[T, E]):
    """Failed result containing an error."""

    error: E
