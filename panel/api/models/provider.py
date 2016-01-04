from django.db import models
from django.contrib import admin


class Provider(models.Model):
    name = models.CharField(max_length=50)
    domain = models.CharField(max_length=50)

    class Meta:
        ordering = ['name']
        app_label = 'api'

    def __str__(self):
        return self.domain


@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    list_display = ('name', 'domain')
