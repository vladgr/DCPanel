from django.db import models
from django.contrib import admin


class Project(models.Model):
    DJANGO = 'DJ'
    PYTHON = 'PY'
    GOLANG = 'GO'
    PHP = 'PHP'
    HTML = 'HTML'

    TYPE_CHOICES = (
        (DJANGO, 'Django'),
        (PYTHON, 'Python'),
        (GOLANG, 'GoLang'),
        (PHP, 'PHP'),
        (HTML, 'HTML')
    )

    PYTHON_CHOICES = (
        ('-', '-'),
        ('2.7', '2.7'),
        ('3.3', '3.3'),
        ('3.4', '3.4'),
        ('3.5', '3.5')
    )

    DJANGO_CHOICES = (
        ('-', '-'),
        ('1.3', '1.3'),
        ('1.4', '1.4'),
        ('1.5', '1.5'),
        ('1.6', '1.6'),
        ('1.7', '1.7'),
        ('1.8', '1.8'),
        ('1.9', '1.9')
    )

    server = models.ForeignKey('Server', null=True, blank=True, default=None)
    type = models.CharField(max_length=4, choices=TYPE_CHOICES)
    name = models.CharField(max_length=50, unique=True)
    domain = models.CharField(max_length=50, blank=True, default='')
    project_dir_server = models.CharField(
        max_length=255, help_text='Absolute path')
    project_dir_local = models.CharField(
        max_length=255, help_text='Absolute path')
    executables = models.TextField(
        blank=True, default='', help_text='Executable files, relative path')
    exclude = models.TextField(
        blank=True, default='', help_text='Exclude dirs, files, relative path')
    is_git = models.BooleanField(default=False, help_text='Git project')
    python_version = models.CharField(
        max_length=3, choices=PYTHON_CHOICES, default='-')
    django_version = models.CharField(
        max_length=3, choices=DJANGO_CHOICES, default='-')
    venv_dir_server = models.CharField(
        max_length=255, blank=True, default='', help_text='Absolute path')
    venv_dir_local = models.CharField(
        max_length=255, blank=True, default='', help_text='Absolute path')
    static_dir_server = models.CharField(
        max_length=255, blank=True, default='', help_text='Absolute path')
    static_dir_local = models.CharField(
        max_length=255, blank=True, default='', help_text='Relative path')
    media_dir_server = models.CharField(
        max_length=255, blank=True, default='', help_text='Absolute path')
    media_dir_local = models.CharField(
        max_length=255, blank=True, default='', help_text='Relative path')
    is_static_dir_separate = models.BooleanField(
        default=False,
        help_text='Store static in separate folder, outside project')
    requirements_dir = models.CharField(
        max_length=255, blank=True, default='', help_text='Relative path')
    uwsgi_port = models.PositiveIntegerField(default=0)
    python_path_server = models.CharField(
        max_length=255, blank=True, default='', help_text='for creating venv')
    python_path_local = models.CharField(
        max_length=255, blank=True, default='', help_text='for creating venv')
    reload_ini_path = models.CharField(max_length=255, blank=True, default='')
    nginx_host_redirect = models.CharField(
        max_length=255, blank=True, default='',
        help_text='For autogenerating config')

    class Meta:
        app_label = 'api'
        ordering = ('type', 'name')

    def __str__(self):
        return self.name

    def textarea_to_list(self, field):
        value = getattr(self, field)
        if not value:
            return []

        l = value.split('\n')
        return [x.strip() for x in l if x.strip()]

    def get_executables(self):
        return self.textarea_to_list('executables')

    def get_exclude(self):
        return self.textarea_to_list('exclude')


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'domain',
        'type',
        'server',
        'project_dir_server',
        'project_dir_local',
        'python_version',
        'django_version',
        'static_dir_server',
        'static_dir_local',
        'uwsgi_port',
        'nginx_host_redirect'
    )
    list_filter = ('server', 'type', 'is_git')
    search_fields = ('name',)
