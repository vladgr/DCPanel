from django.db import models
from django.contrib import admin


class Country(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = 'countries'
        ordering = ['name']
        app_label = 'api'

    def __str__(self):
        return self.name


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name',)
