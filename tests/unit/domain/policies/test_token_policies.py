from src.domain.policies.token import SubRequiredPolicy
from src.domain.value_objects.claims import Claims
from src.domain.value_objects.issue import IssueCode

from src.bootstrap import AuthContainer


def test_policy_should_find_missed_sub(container: AuthContainer):
    policy = SubRequiredPolicy()

    claims = container.claims_factory().access_claims('1')
    issues = list(policy.evaluate(claims))
    assert not issues

    claims_dict = claims.as_dict()
    del claims_dict['sub']
    claims = Claims(**claims_dict)
    issues = list(policy.evaluate(claims))

    assert len(issues) == 1
    assert issues[0].code is IssueCode.REQUIRED_SUB
