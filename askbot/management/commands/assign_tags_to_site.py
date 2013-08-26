from askbot import models
from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        site_id = args[0]
        site = Site.objects.get(id=site_id)
        for tag in models.Tag.objects.all().iterator():
            old_links = models.TagToSite.objects.filter(tag=tag)
            old_links.delete()
            new_link = models.TagToSite(tag=tag, site=site)
            new_link.save()
