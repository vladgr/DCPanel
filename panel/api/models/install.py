from django.db import models
from django.contrib import admin

from .conf import Conf


class Install(models.Model):
    server = models.ForeignKey('Server')
    item = models.CharField(max_length=20, choices=Conf.ITEM_CHOICES)

    class Meta:
        app_label = 'api'
        ordering = ('server', 'item')

    def __str__(self):
        return str(self.id)

    def required_files(self):
        if self.item == 'bash':
            return ['bash_aliases', 'bashrc']

        elif self.item == 'iptables':
            return [
                'ip6tables.service',
                'iptables.service',
                'myip6tables',
                'myip6tables-stop',
                'myiptables',
                'myiptables-stop'
            ]

        elif self.item == 'mysql':
            return ['myconf.cnf']

        elif self.item == 'php':
            return ['php.ini', 'php-fpm.conf', 'www.conf']

        elif self.item == 'postfix':
            return [
                '10-auth.conf',
                '10-mail.conf',
                '10-master.conf',
                '10-ssl.conf',
                'auth-sql.conf.ext',
                'dovecot.conf',
                'TrustedHosts',
                'opendkim',
                'opendkim.conf',
                'main.cf',
                'master.cf',
                'local.cf',
                'spamassassin'
            ]

        elif self.item == 'postgresql':
            return ['pg_hba.conf']

        elif self.item == 'supervisor':
            return ['supervisord.conf', 'supervisord.service']

        elif self.item == 'squid':
            return ['interfaces', 'squid.conf']

        return []


@admin.register(Install)
class InstallAdmin(admin.ModelAdmin):
    list_display = ('server', 'item')
    list_filter = ('server', 'item')


class InstallInline(admin.TabularInline):
    model = Install
    extra = 0
    readonly_fields = ('item',)
