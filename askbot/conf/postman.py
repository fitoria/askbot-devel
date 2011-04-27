"""
External service key settings
"""
from askbot.conf.settings_wrapper import settings
from askbot.deps import livesettings
from django.utils.translation import ugettext as _
from django.conf import settings as django_settings

POSTMAN = livesettings.ConfigurationGroup(
                    'POSTMAN',
                    _('Private messaging settings')
                )

settings.register(
    livesettings.BooleanValue(
        POSTMAN,
        'POSTMAN_AUTO_MODERATE_AS',
        default = True,
        description=_('Do not moderate messages'),
    )
)

settings.register(
    livesettings.BooleanValue(
        POSTMAN,
        'POSTMAN_DISALLOW_ANONYMOUS',
        default = True,
        description=_('Do not allow anonymous'),
    )
)

settings.register(
    livesettings.BooleanValue(
        POSTMAN,
        'POSTMAN_DISALLOW_COPIES_ON_REPLY',
        default = True,
        description=_('Do not allow copies on reply'),
    )
)

settings.register(
    livesettings.BooleanValue(
        POSTMAN,
        'POSTMAN_DISALLOW_MULTIRECIPIENTS',
        default = False,
        description=_('Do not allow multiple recipients on a message'),
    )
)
