from django.db import models
from django.contrib import admin

from .base import TextareaXL


class Conf(models.Model):
    SERVER = 'S'
    PROJECT = 'P'
    TYPE_CHOICES = ((SERVER, 'Server'), (PROJECT, 'Project'))

    BASH = 'bash'
    CRON = 'cron'
    GOLANG = 'golang'
    IPTABLES = 'iptables'
    MYSQL = 'mysql'
    NGINX = 'nginx'
    PHP = 'php'
    POSTFIX = 'postfix'
    POSTGRESQL = 'postgresql'
    PYTHON2 = 'python2'
    PYTHON3 = 'python3'
    REDIS = 'redis'
    SUPERVISOR = 'supervisor'
    SQUID = 'squid'

    ITEM_CHOICES = (
        (BASH, 'Bash'),
        (CRON, 'Cron'),
        (GOLANG, 'GoLang'),
        (IPTABLES, 'IPTables'),
        (MYSQL, 'MySQL'),
        (NGINX, 'Nginx'),
        (PHP, 'PHP'),
        (POSTFIX, 'Postfix'),
        (POSTGRESQL, 'PostgreSQL'),
        (PYTHON2, 'Python 2'),
        (PYTHON3, 'Python 3'),
        (REDIS, 'Redis'),
        (SUPERVISOR, 'Supervisor'),
        (SQUID, 'Squid')
    )

    server = models.ForeignKey('Server', null=True, blank=True, default=None)
    project = models.ForeignKey('Project', null=True, blank=True, default=None)
    type = models.CharField(max_length=1, choices=TYPE_CHOICES)
    item = models.CharField(max_length=20, choices=ITEM_CHOICES)
    filename = models.CharField(max_length=50)
    data = models.TextField(help_text='file data', blank=True, default='')
    comment = models.CharField(max_length=50, blank=True, default='')
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Config'
        verbose_name_plural = 'Configs'
        app_label = 'api'
        ordering = ('server', 'project', 'item', 'comment', 'filename')


@admin.register(Conf)
class ConfAdmin(admin.ModelAdmin):
    list_display = (
        'server',
        'project',
        'item',
        'comment',
        'filename',
        'is_active'
    )
    list_display_links = ('server', 'project')
    list_filter = ('server', 'type', 'item', 'project')
    formfield_overrides = {models.TextField: {'widget': TextareaXL}}
    search_fields = ('project__name', 'server__code', 'filename')

    def add_view(self, request, extra_context=None):
        title = 'Add either "Server" or "Project" config.'
        extra_context = extra_context or {}
        extra_context['title'] = title
        self.fields = (
            'server',
            'project',
            'item',
            'comment',
            'filename',
            'is_active',
            'data'
        )
        self.readonly_fields = ()
        return super().add_view(request, extra_context=extra_context)

    def change_view(self, request, object_id):
        self.readonly_fields = ('server', 'project', 'item', 'filename')

        obj = Conf.objects.get(id=object_id)
        fields = ('item', 'comment', 'filename', 'is_active', 'data')
        if obj.type == 'S':
            self.fields = ('server',) + fields
        elif obj.type == 'P':
            self.fields = ('project',) + fields
        return super().change_view(request, object_id)

    def save_model(self, request, obj, form, change):
        """Automatically determines the type of config"""
        if obj.server:
            obj.type = Conf.SERVER

        if obj.project:
            obj.type = Conf.PROJECT
            obj.server = None

        obj.save()


class ConfInline(admin.TabularInline):
    model = Conf
    extra = 0
    fields = ('item', 'filename')
    readonly_fields = ('item', 'filename')
    show_change_link = True
