# Create your models here.
from locale import currency
from statistics import mode

from django.db import models

from core.misc.zap_crawler import ZapCrawler


class TimeStampedModel(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta():
        abstract = True


class EstimateRequest(TimeStampedModel):

    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    url = models.URLField()

    price = models.PositiveSmallIntegerField(null=True, blank=True)
    condominium = models.PositiveSmallIntegerField(null=True, blank=True)
    iptu = models.PositiveSmallIntegerField(null=True, blank=True)
    currency = models.CharField(max_length=5, null=True, blank=True)

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'estimate_request'
        managed = True
        verbose_name = 'Estimate Request'
        verbose_name_plural = 'Estimate Requests'

    def save(self, *args, **kwargs):
        self._set_pricing_variables()
        super(EstimateRequest, self).save(*args, **kwargs)

    def _set_pricing_variables(self):
        crawler = ZapCrawler(self.url)
        data = crawler.get_data()
        for key, value in data.items():
            setattr(self, key, value)
