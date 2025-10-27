from src.domain.policies.password import PasswordNotInBlacklistPolicy
from src.domain.value_objects.account import Password


def test_blacklist_policy_rejects_blacklisted_password_and_accepts_allowed_password():
    policy = PasswordNotInBlacklistPolicy({"password", "123456"})

    rejected = policy.validate(Password("password"))
    accepted = policy.validate(Password("strong_pass"))

    assert not rejected
    assert accepted
