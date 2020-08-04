from django.conf import settings
from django.db import models

from toolbox.geolocator import download_ip2location_database


class IP2LocationDBUpdate(models.Model):
    db_code = models.CharField(verbose_name='Database code',
                               max_length=20,
                               blank=True,
                               default=getattr(settings, "IP2LOCATION_DBCODE"))
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(verbose_name='Last Update Status',
                                 default=False)

    class Meta:
        ordering = ['-updated_on']
        verbose_name = 'IP2Location database'
        verbose_name_plural = 'IP2Location databases'

    def __str__(self):
        return self.db_code

    def save(self, *args, **kwargs):
        self.db_code, self.status = download_ip2location_database()
        super(IP2LocationDBUpdate, self).save(*args, **kwargs)


class FAQs(models.Model):
    title = models.CharField(max_length=200, help_text='Enter question title')
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_on']
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQs'

    def __str__(self):
        return self.title
