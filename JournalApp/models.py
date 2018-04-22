from __future__ import unicode_literals
from django.db import models
from django.conf import settings

# Create your models here.
from django.urls import reverse
from rest_framework.reverse import reverse as api_reverse

class Journal(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    title = models.CharField(max_length=50, null=True)
    quote = models.TextField(null=True, blank=True)
    grateful_for = models.TextField(null=True, blank=True)
    today_view = models.TextField(null=True, blank=True)
    today_affrimation = models.TextField(null=True, blank=True)
    happened_today = models.TextField(null=True, blank=True)

    created_at = models.DateField(blank=True, auto_now_add=True)

    # This is the detail view of single journal with respect to api
    def get_api_url(self, request=None):
        return api_reverse("api:journalCrud", kwargs={'id': self.pk}, request=request) # first given is the app url then the method url, with kwargs of the url


