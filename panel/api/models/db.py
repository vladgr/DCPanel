from django.db import models
from django.contrib import admin

from .user import User, UserInline


class Db(models.Model):
    SERVER = 'S'
    PROJECT = 'P'
    TYPE_CHOICES = ((SERVER, 'Server'), (PROJECT, 'Project'))

    MYSQL = 'M'
    POSTGRESQL = 'P'
    SQLITE = 'S'
    DB_CHOICES = (
        (MYSQL, 'MySQL'),
        (POSTGRESQL, 'PostgreSQL'),
        (SQLITE, 'SQLite')
    )

    server = models.ForeignKey('Server', null=True, blank=True, default=None)
    project = models.ForeignKey('Project', null=True, blank=True, default=None)
    type = models.CharField(max_length=1, choices=TYPE_CHOICES)
    type_db = models.CharField(
        max_length=3, choices=DB_CHOICES, verbose_name='database type')
    name = models.CharField(
        max_length=50, blank=True, default='', help_text='for project')
    version = models.CharField(
        max_length=50, blank=True, default='', help_text='for server')
    remote_access = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'database'
        verbose_name_plural = 'databases'
        app_label = 'api'
        ordering = ['-type', 'type_db', 'name']

    def __str__(self):
        if self.type == self.PROJECT:
            return self.name

        return '{}: {} {}'.format(
            self.server.code, self.get_type_db_display(), self.version)

    def get_user(self):
        """Return dict of users for server and single dict for project"""
        if self.type == Db.SERVER:
            users = User.objects.filter(
                type=User.DB,
                db_id=self.id,
                is_active=True
            )
            return {u.name: u.get_password() for u in users}

        if self.type == Db.PROJECT:
            user = User.objects.get(db_id=self.id)
            return {'name': user.name, 'password': user.get_password()}

    def get_server_ip(self):
        """Returns main server IP address"""
        if self.type == Db.SERVER:
            return self.server.get_main_ip()

        server = self.project.server
        if server:
            return server.get_main_ip()

        return ''

    def get_project_name(self):
        """Returns project name"""
        if self.type == Db.SERVER:
            return ''

        return self.project.name


@admin.register(Db)
class DbAdmin(admin.ModelAdmin):
    inlines = (UserInline,)
    list_display = ('id', 'server', 'project', 'name', 'version', 'type_db')
    list_filter = ('type', 'type_db')
    search_fields = ('project__name', 'name')

    def add_view(self, request, extra_context=None):
        title = 'Add either "Server" or "Project" database.'
        extra_context = extra_context or {}
        extra_context['title'] = title

        self.fields = (
            'type_db',
            'server',
            'version',
            'project',
            'name',
            'remote_access'
        )
        self.readonly_fields = ()
        return super().add_view(request, extra_context=extra_context)

    def change_view(self, request, object_id):
        self.readonly_fields = ('server', 'project', 'type', 'type_db', 'name')

        obj = Db.objects.get(id=object_id)
        if obj.type == Db.SERVER:
            self.fields = (
                'server',
                'type_db',
                'version',
                'remote_access'
            )
        elif obj.type == Db.PROJECT:
            self.fields = (
                'project',
                'type_db',
                'name',
                'remote_access'
            )
        return super().change_view(request, object_id)

    def save_model(self, request, obj, form, change):
        """Automatically determines the type of database"""
        if obj.server:
            obj.type = Db.SERVER

        if obj.project:
            obj.type = Db.PROJECT
            obj.server = None

        obj.save()
