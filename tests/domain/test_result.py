"""Tests for Result pattern."""

import pytest

from src.domain.result import Failure, Result, Success


class TestResult:
    """Tests for Result pattern."""

    def test_success_is_success(self) -> None:
        """Test that Success returns True for is_success."""
        result: Result[int, str] = Success(42)

        assert result.is_success() is True
        assert result.is_failure() is False

    def test_failure_is_failure(self) -> None:
        """Test that Failure returns True for is_failure."""
        result: Result[int, str] = Failure('error')

        assert result.is_failure() is True
        assert result.is_success() is False

    def test_success_unwrap_returns_value(self) -> None:
        """Test that unwrap returns value for Success."""
        result: Result[int, str] = Success(42)

        assert result.unwrap() == 42

    def test_failure_unwrap_raises(self) -> None:
        """Test that unwrap raises for Failure."""
        result: Result[int, str] = Failure('error')

        with pytest.raises(ValueError, match='Called unwrap on Failure'):
            result.unwrap()

    def test_success_unwrap_or_returns_value(self) -> None:
        """Test that unwrap_or returns value for Success."""
        result: Result[int, str] = Success(42)

        assert result.unwrap_or(0) == 42

    def test_failure_unwrap_or_returns_default(self) -> None:
        """Test that unwrap_or returns default for Failure."""
        result: Result[int, str] = Failure('error')

        assert result.unwrap_or(0) == 0

    def test_success_map_transforms_value(self) -> None:
        """Test that map transforms Success value."""
        result: Result[int, str] = Success(42)

        mapped = result.map(lambda x: x * 2)

        assert isinstance(mapped, Success)
        assert mapped.unwrap() == 84

    def test_failure_map_returns_failure(self) -> None:
        """Test that map on Failure returns Failure unchanged."""
        result: Result[int, str] = Failure('error')

        mapped = result.map(lambda x: x * 2)

        assert isinstance(mapped, Failure)
        assert mapped.error == 'error'  # type: ignore[attr-defined]

    def test_success_map_error_returns_success(self) -> None:
        """Test that map_error on Success returns Success unchanged."""
        result: Result[int, str] = Success(42)

        mapped = result.map_error(lambda e: e.upper())

        assert isinstance(mapped, Success)
        assert mapped.value == 42  # type: ignore[attr-defined]

    def test_failure_map_error_transforms_error(self) -> None:
        """Test that map_error transforms Failure error."""
        result: Result[int, str] = Failure('error')

        mapped = result.map_error(lambda e: e.upper())

        assert isinstance(mapped, Failure)
        assert mapped.error == 'ERROR'  # type: ignore[attr-defined]

    def test_success_and_then_chains(self) -> None:
        """Test that and_then chains Success operations."""
        result: Result[int, str] = Success(42)

        chained = result.and_then(lambda x: Success(x * 2))

        assert isinstance(chained, Success)
        assert chained.unwrap() == 84

    def test_success_and_then_can_return_failure(self) -> None:
        """Test that and_then can return Failure."""
        result: Result[int, str] = Success(42)

        chained = result.and_then(lambda x: Failure('error'))

        assert isinstance(chained, Failure)
        assert chained.error == 'error'  # type: ignore[attr-defined]

    def test_failure_and_then_returns_failure(self) -> None:
        """Test that and_then on Failure returns Failure unchanged."""
        result: Result[int, str] = Failure('error')

        chained = result.and_then(lambda x: Success(x * 2))

        assert isinstance(chained, Failure)
        assert chained.error == 'error'  # type: ignore[attr-defined]

    def test_result_chaining(self) -> None:
        """Test chaining multiple Result operations."""
        result: Result[int, str] = Success(10)

        final = (
            result.map(lambda x: x + 5)  # Success(15)
            .and_then(lambda x: Success(x * 2))  # Success(30)
            .map(lambda x: x - 10)  # Success(20)
        )

        assert isinstance(final, Success)
        assert final.unwrap() == 20
