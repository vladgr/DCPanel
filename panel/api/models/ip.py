from django.db import models
from django.contrib import admin

IP_TYPES = [(4, 'IPv4'), (6, 'IPv6')]


class Ip(models.Model):
    server = models.ForeignKey('Server', related_name='ips')
    type = models.SmallIntegerField(choices=IP_TYPES)
    value = models.GenericIPAddressField()
    is_main = models.BooleanField(default=False, help_text='main server Ip')

    class Meta:
        verbose_name = 'Ip Address'
        verbose_name_plural = 'Ip Addresses'
        app_label = 'api'
        ordering = ('server', 'type', '-is_main')

    def __str__(self):
        return self.value


@admin.register(Ip)
class IpAdmin(admin.ModelAdmin):
    list_display = ('server', 'type', 'value', 'is_main')
    list_filter = ('server', 'type')


class IpInline(admin.TabularInline):
    model = Ip
    extra = 0
