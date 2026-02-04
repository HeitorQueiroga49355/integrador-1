from user.models import Profile


def get_default_page_alias_by_user(user):
    if not user.is_authenticated:
        return 'login'
    page_alias = 'pesquisador-editais'
    if user.profile.role == Profile.Role.MANAGER:
        page_alias = 'proposals'
    elif user.profile.role == Profile.Role.EVALUATOR:
        page_alias = 'my_evaluations'
    return page_alias