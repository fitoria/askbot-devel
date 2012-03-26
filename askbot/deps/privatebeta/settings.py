from django.conf import settings

PRIVATEBETA_NEVER_ALLOW_VIEWS = getattr(settings, 'PRIVATEBETA_NEVER_ALLOW_VIEWS',
        ['askbot.deps.django_authopenid.views.register',
         'askbot.deps.django_authopenid.views.decorated', ])
PRIVATEBETA_ALWAYS_ALLOW_VIEWS = getattr(settings, 'PRIVATEBETA_ALWAYS_ALLOW_VIEWS', [])
PRIVATEBETA_ALWAYS_ALLOW_MODULES = getattr(settings, 'PRIVATEBETA_ALWAYS_ALLOW_MODULES',
        ['askbot.views.readers', 'askbot.views.meta',
         'askbot.views.users',
         'askbot.views.avatar_views',
         'askbot.views.writers',
         'askbot.views.commands',
         'askbot.deps.django_authopenid.views',
         ])
