"""Tests for LoginService application service."""

import pytest

from src.domain.entities import Account
from src.domain.value_objects import AccessToken, Email, Password, RefreshToken

from src.application.exceptions import InvalidCredentialsError
from src.application.services.login import LoginResult, LoginService

from tests.application.conftest import (
    MockJwtService,
    MockPasswordHasher,
    MockUnitOfWork,
)


class TestLoginService:
    """Tests for LoginService."""

    @pytest.mark.asyncio
    async def test_successful_login(
        self,
        mock_uow: MockUnitOfWork,
        mock_password_hasher: MockPasswordHasher,
        mock_jwt_service: MockJwtService,
        sample_email: Email,
        sample_password: Password,
        sample_account: Account,
    ) -> None:
        """Test successful login with correct credentials."""
        # Add account to repository
        mock_uow.accounts.accounts[sample_email.value] = sample_account

        service = LoginService(
            uow=mock_uow,
            password_hasher=mock_password_hasher,
            jwt_service=mock_jwt_service,
        )

        result = await service.login(email=sample_email, password=sample_password)

        assert isinstance(result, LoginResult)
        assert isinstance(result.access_token, AccessToken)
        assert isinstance(result.refresh_token, RefreshToken)

        # Verify password was verified
        mock_password_hasher.verify.assert_called_once_with(
            sample_password, sample_account.password_hash
        )

        # Verify tokens were issued
        mock_jwt_service.issue_access.assert_called_once()
        mock_jwt_service.issue_refresh.assert_called_once()

    @pytest.mark.asyncio
    async def test_login_with_nonexistent_email(
        self,
        mock_uow: MockUnitOfWork,
        mock_password_hasher: MockPasswordHasher,
        mock_jwt_service: MockJwtService,
        sample_email: Email,
        sample_password: Password,
    ) -> None:
        """Test login fails with non-existent email."""
        service = LoginService(
            uow=mock_uow,
            password_hasher=mock_password_hasher,
            jwt_service=mock_jwt_service,
        )

        with pytest.raises(InvalidCredentialsError, match='Account does not found'):
            await service.login(email=sample_email, password=sample_password)

        # Verify no tokens were issued
        mock_jwt_service.issue_access.assert_not_called()
        mock_jwt_service.issue_refresh.assert_not_called()

    @pytest.mark.asyncio
    async def test_login_with_incorrect_password(
        self,
        mock_uow: MockUnitOfWork,
        mock_password_hasher: MockPasswordHasher,
        mock_jwt_service: MockJwtService,
        sample_email: Email,
        sample_account: Account,
    ) -> None:
        """Test login fails with incorrect password."""
        # Add account to repository
        mock_uow.accounts.accounts[sample_email.value] = sample_account

        service = LoginService(
            uow=mock_uow,
            password_hasher=mock_password_hasher,
            jwt_service=mock_jwt_service,
        )

        # Use wrong password
        wrong_password = Password('WrongPassword123!')

        with pytest.raises(InvalidCredentialsError, match='Incorrect password'):
            await service.login(email=sample_email, password=wrong_password)

        # Verify password was verified
        mock_password_hasher.verify.assert_called_once()

        # Verify no tokens were issued
        mock_jwt_service.issue_access.assert_not_called()
        mock_jwt_service.issue_refresh.assert_not_called()

    @pytest.mark.asyncio
    async def test_login_returns_correct_tokens(
        self,
        mock_uow: MockUnitOfWork,
        mock_password_hasher: MockPasswordHasher,
        mock_jwt_service: MockJwtService,
        sample_email: Email,
        sample_password: Password,
        sample_account: Account,
    ) -> None:
        """Test that login returns tokens with correct format."""
        # Add account to repository
        mock_uow.accounts.accounts[sample_email.value] = sample_account

        service = LoginService(
            uow=mock_uow,
            password_hasher=mock_password_hasher,
            jwt_service=mock_jwt_service,
        )

        result = await service.login(email=sample_email, password=sample_password)

        # Verify tokens contain expected data
        assert f'access_token_for_{sample_email.value}' in result.access_token.value
        assert f'refresh_token_for_{sample_email.value}' in result.refresh_token.value

    @pytest.mark.asyncio
    async def test_login_with_inactive_account(
        self,
        mock_uow: MockUnitOfWork,
        mock_password_hasher: MockPasswordHasher,
        mock_jwt_service: MockJwtService,
        sample_email: Email,
        sample_password: Password,
        sample_account: Account,
    ) -> None:
        """Test login with inactive account still works.
        
        Note: Current implementation doesn't check is_active status,
        this test documents that behavior.
        """
        # Make account inactive
        sample_account.is_active = False
        mock_uow.accounts.accounts[sample_email.value] = sample_account

        service = LoginService(
            uow=mock_uow,
            password_hasher=mock_password_hasher,
            jwt_service=mock_jwt_service,
        )

        # Should succeed - current implementation doesn't check is_active
        result = await service.login(email=sample_email, password=sample_password)

        assert isinstance(result, LoginResult)
        assert isinstance(result.access_token, AccessToken)
        assert isinstance(result.refresh_token, RefreshToken)

    @pytest.mark.asyncio
    async def test_login_passes_empty_scopes_to_access_token(
        self,
        mock_uow: MockUnitOfWork,
        mock_password_hasher: MockPasswordHasher,
        mock_jwt_service: MockJwtService,
        sample_email: Email,
        sample_password: Password,
        sample_account: Account,
    ) -> None:
        """Test that login passes empty scopes to access token."""
        # Add account to repository
        mock_uow.accounts.accounts[sample_email.value] = sample_account

        service = LoginService(
            uow=mock_uow,
            password_hasher=mock_password_hasher,
            jwt_service=mock_jwt_service,
        )

        await service.login(email=sample_email, password=sample_password)

        # Verify issue_access was called with empty scopes
        args, kwargs = mock_jwt_service.issue_access.call_args
        assert args[0] == sample_account
        assert args[1] == [] or kwargs.get('scopes') == []
