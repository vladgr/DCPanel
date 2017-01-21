from django.db import models
from django.contrib import admin

from .conf import ConfInline
from .install import InstallInline
from .ip import Ip, IpInline


class Server(models.Model):
    DEBIAN_8 = 'D8'
    UBUNTU_14 = 'U14'
    UBUNTU_16 = 'U16'
    CENTOS_7 = 'C7'
    AMAZON = 'AM'
    HEROKU = 'HK'

    TYPE_CHOICES = (
        (DEBIAN_8, 'Debian 8'),
        (UBUNTU_14, 'Ubuntu 14'),
        (UBUNTU_16, 'Ubuntu 16'),
        (CENTOS_7, 'Centos 7'),
        (AMAZON, 'Amazon'),
        (HEROKU, 'Heroku')
    )

    country = models.ForeignKey('Country')
    provider = models.ForeignKey(
        'Provider', null=True, blank=True, default=None)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    code = models.CharField(max_length=20, unique=True)
    server_main_user = models.CharField(max_length=50)
    nginx_name = models.CharField(
        max_length=20, blank=True, default='',
        help_text='different on debian/centos')
    control_dir = models.CharField(
        max_length=255, blank=True, default='',
        help_text='folder for control scripts')

    class Meta:
        app_label = 'api'
        ordering = ['code']

    def __str__(self):
        return self.code

    def get_main_ip(self):
        return Ip.objects.filter(server_id=self.id, is_main=True).first()

    def get_admin_copy_config_url(self):
        return '/admin/api/custom/copy_config/'

    def get_admin_check_server_configs_urls(self):
        return '/admin/api/custom/check_server_configs/{}/'.format(self.id)

    @staticmethod
    def get_admin_urls():
        sp = []
        sp.append((r'^api/custom/copy_config/$', 'copy_config'))
        sp.append(
            (r'^api/custom/check_server_configs/(?P<server_id>\d+)/$',
                'check_server_configs'))
        return sp


@admin.register(Server)
class ServerAdmin(admin.ModelAdmin):
    inlines = (IpInline, InstallInline, ConfInline)
    list_display = (
        'code',
        'provider',
        'country',
        'type',
        'server_main_user',
        'nginx_name',
        'control_dir'
    )
