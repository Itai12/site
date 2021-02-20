from .common import *

PROLOGIN_SEMIFINAL_MODE = True

# How much time spent on a problem becomes concerning
# Format: a tuple of (warning amount, danger amount), amounts in seconds
SEMIFINAL_CONCERNING_TIME_SPENT = (30 * 60, 45 * 60)

# We won't use those in semifinal
RECAPTCHA_PUBLIC_KEY = ''
RECAPTCHA_PRIVATE_KEY = ''

MIDDLEWARE = (
    'django_prometheus.middleware.PrometheusBeforeMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',

    # French by default for semifinals, avoid browsers misconfigurations
    # 'django.middleware.locale.LocaleMiddleware',

    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'semifinal.middleware.SemifinalMiddleware',
)

INSTALLED_APPS = (
    # Django
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'social_django',

    # Vendor
    'adminsortable',
    'bootstrapform',
    'django_bootstrap_breadcrumbs',
    'rules.apps.AutodiscoverRulesConfig',

    # Prologin apps
    'semifinal',  # must stay at the top
    'prologin',
    'centers',
    'contest',
    'problems',
    'schools',
    'users',

    # Django and vendor, at the bottom for template overriding
    'django.contrib.admin',
)

ROOT_URLCONF = 'semifinal.urls'

AUTHENTICATION_BACKENDS = (
    'prologin.backends.ModelBackend',
    'rules.permissions.ObjectPermissionBackend',
    'semifinal.oidc.ProloginOIDCBackend',
)

SOCIAL_AUTH_PIPELINE = (
    "social_core.pipeline.social_auth.social_details",
    "social_core.pipeline.social_auth.social_uid",
    "social_core.pipeline.social_auth.auth_allowed",
    "social_core.pipeline.social_auth.social_user",
    "social_core.pipeline.user.get_username",
    #"social_core.pipeline.user.create_user",
    "semifinal.oidc.create_user",
    "social_core.pipeline.social_auth.associate_user",
    "social_core.pipeline.social_auth.load_extra_data",
    "semifinal.oidc.save_all_claims_as_extra_data",
    "social_core.pipeline.user.user_details",
    "semifinal.oidc.apply_upstream_security_clearances",
)

SOCIAL_AUTH_PROLOGIN_SCOPE = [
    "email",
    "contest",
    "security_clearance",
]
