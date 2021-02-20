from social_core.backends.open_id_connect import OpenIdConnectAuth
from users.models import ProloginUser
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings


class ProloginOIDCBackend(OpenIdConnectAuth):
    name = "prologin"
    OIDC_ENDPOINT = settings.PROLOGIN_OIDC_ENDPOINT


def save_all_claims_as_extra_data(
    response, storage, social=None, *_args, **_kwargs
):
    """Update user extra-data using data from provider."""
    if not social:
        return

    social.extra_data = response
    storage.user.changed(social)

def create_user(strategy, details, user=None, response=None, social=None, *args, **kwargs):
    if response and response.get('is_staff'):
        print("user is staff")
        return {
            'is_new': True,
            'user': strategy.create_user(**{
                'username': response.get('nickname'),
                'first_name': response.get('given_name'),
                'last_name': response.get('family_name'),
                'email': response.get('email'),
                'is_staff': True,
                'is_superuser': response.get('is_superuser'),
            })
        }

    try:
        pu = ProloginUser.objects.get(id=response['sub'])
        return {
            'social': social,
            'user': pu,
            'new_association': True
        }
    except ObjectDoesNotExist:
        return False

    return False


def apply_upstream_security_clearances(
    storage, backend, details, social=None, user=None, *_args, **_kwargs
):
    if not user or backend.name != "prologin":
        return

    is_staff = social.extra_data.get("is_staff", False)
    is_superuser = social.extra_data.get("is_superuser", False)
    user.is_staff = is_staff
    user.is_superuser = is_superuser
    storage.user.changed(user)
