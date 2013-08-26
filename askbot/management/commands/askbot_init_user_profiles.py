from django.core.management.base import NoArgsCommand
from askbot.models import User, init_askbot_user_profile

class Command(NoArgsCommand):
    """a command to initialize missing askbot user profiles"""
    def handle_noargs(self, **kwargs):
        for user in User.objects.all():
            try:
                init_askbot_user_profile(user)
            except:
                pass
