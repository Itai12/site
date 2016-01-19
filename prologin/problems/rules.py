from django.conf import settings
import rules


@rules.predicate
def is_challenge_displayable(user, challenge):
    if settings.PROLOGIN_SEMIFINAL_MODE and not user.is_authenticated():
        return False
    return ((not settings.PROBLEMS_CHALLENGE_WHITELIST or challenge.name in settings.PROBLEMS_CHALLENGE_WHITELIST) and
            challenge.displayable)


@rules.predicate
def can_view_problem(user, problem):
    displayable = is_challenge_displayable(user, problem.challenge)
    if not displayable:
        return False
    if settings.PROLOGIN_SEMIFINAL_MODE:
        from contest.models import Contestant
        return problem in Contestant.objects.get(user=user, edition=settings.PROLOGIN_EDITION).available_semifinal_problems()
    return displayable


@rules.predicate
def is_code_submission_owner(user, code):
    return user == code.submission.user


# Permissions
rules.add_perm('problems.view_challenge', rules.is_staff | is_challenge_displayable)
rules.add_perm('problems.view_problem', rules.is_staff | can_view_problem)
rules.add_perm('problems.view_code_submission', rules.is_staff | is_code_submission_owner)
rules.add_perm('problems.create_problem_code_submission', rules.is_staff | can_view_problem)
