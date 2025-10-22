from dataclasses import dataclass, field
from uuid import UUID

from src.domain.value_objects import Email, PasswordHash, Role


@dataclass
class Account:
    """Aggregate Root for authentication and authorization.
    
    Account encapsulates all business logic related to user accounts,
    including password management, activation status, and roles.
    It maintains invariants and emits domain events when state changes.
    """

    identifier: UUID | None
    email: Email
    password_hash: PasswordHash
    is_active: bool = True
    username: str | None = field(default=None)
    roles: list[Role] = field(default_factory=list)

    def change_password(
        self, new_password_hash: PasswordHash
    ) -> 'AccountPasswordChanged':
        """Change account password.
        
        Args:
            new_password_hash: New password hash to set
            
        Returns:
            Domain event indicating password was changed
            
        Raises:
            ValueError: If account is not active
        """
        if not self.is_active:
            msg = 'Cannot change password for inactive account'
            raise ValueError(msg)

        from src.domain.events import AccountPasswordChanged

        self.password_hash = new_password_hash
        return AccountPasswordChanged(email=self.email)

    def activate(self) -> 'AccountActivated':
        """Activate the account.
        
        Returns:
            Domain event indicating account was activated
            
        Raises:
            ValueError: If account is already active
        """
        if self.is_active:
            msg = 'Account is already active'
            raise ValueError(msg)

        from src.domain.events import AccountActivated

        self.is_active = True
        return AccountActivated(email=self.email)

    def deactivate(self) -> 'AccountDeactivated':
        """Deactivate the account.
        
        Returns:
            Domain event indicating account was deactivated
            
        Raises:
            ValueError: If account is already inactive
        """
        if not self.is_active:
            msg = 'Account is already inactive'
            raise ValueError(msg)

        from src.domain.events import AccountDeactivated

        self.is_active = False
        return AccountDeactivated(email=self.email)

    def add_role(self, role: Role) -> None:
        """Add a role to the account.
        
        Args:
            role: Role to add
            
        Raises:
            ValueError: If role already exists
        """
        if role in self.roles:
            msg = f'Role {role} already exists'
            raise ValueError(msg)
        self.roles.append(role)

    def remove_role(self, role: Role) -> None:
        """Remove a role from the account.
        
        Args:
            role: Role to remove
            
        Raises:
            ValueError: If role does not exist
        """
        if role not in self.roles:
            msg = f'Role {role} does not exist'
            raise ValueError(msg)
        self.roles.remove(role)

    def has_role(self, role: Role) -> bool:
        """Check if account has a specific role.
        
        Args:
            role: Role to check
            
        Returns:
            True if account has the role, False otherwise
        """
        return role in self.roles
