from django.db import models
from askbot.models.post import Post
from askbot.models.user import Group
from askbot.models.question import Thread
from django.contrib.sites.models import Site
from django.utils.translation import ugettext as _

class Space(models.Model):
    name = models.CharField(max_length=100)
    questions = models.ManyToManyField(Thread)
    description = models.ForeignKey(Post)

    class Meta:
        app_label = 'askbot'

    def __unicode__(self):
        return "Space %s" % self.name

class Feed(models.Model):
    #TODO: url should never change add validation.
    url = models.CharField(max_length=50)
    redirect = models.ForeignKey('self')
    default_space = models.ForeignKey(Space)

    site = models.ForeignKey(Site)

    class Meta:
        app_label = 'askbot'

    def __unicode__(self):
        return "Feed %s" % self.url

class FeedToSpace(models.Model):
    space = models.ForeignKey(Space)
    feed = models.ForeignKey(Feed)

    class Meta:
        app_label = 'askbot'
        unique_together = ('space', 'feed')

class GroupToSpace(models.Model):
    group = models.ForeignKey(Group)
    space = models.ForeignKey(Space)

    class Meta:
        app_label = 'askbot'
        unique_together = ('space', 'group')
