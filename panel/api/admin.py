from django.contrib import admin
from django.contrib import messages
from django.conf.urls import patterns, url
from django.db import connection

from .bm import Db, Ip, Project, Server, User
import api.views_admin as views_admin


def index(self, request, *args, **kwargs):
    extra_context = {}

    errors = validate_server_db1()
    errors += validate_server_db2()
    errors += validate_server_db3()
    errors += validate_project_db1()
    errors += validate_project_db2()
    errors += validate_uwsgi()
    errors += validate_server_ip()
    errors += validate_project_dirs()

    if errors:
        for e in errors:
            messages.warning(request, e)

    return admin.site.__class__.index(
        self, request, extra_context=extra_context, *args, **kwargs)
admin.site.index = index.__get__(admin.site, admin.site.__class__)


def validate_server_db1():
    """Server may have only single database of particular type"""
    cursor = connection.cursor()

    query = """
        SELECT MAX(counted) FROM
        (
            SELECT COUNT(*) AS counted
            FROM api_db
            WHERE type = "S"
            GROUP BY server_id,type_db
        ) AS counts;
        """

    cursor.execute(query)
    res = cursor.fetchone()[0]
    if res > 1:
        return [
            'Server may have only single database of particular type!']
    return []


def validate_server_db2():
    """Each server MySQL database should have root user"""
    ids = Db.objects.filter(
        type='S', type_db=Db.MYSQL).values_list('id', flat=True)
    for id in ids:
        res = User.objects.filter(db_id=id, name='root').count()
        if res != 1:
            return ['Each server\'s MySQL db should have single "root" user!']
    return []


def validate_server_db3():
    """Each server Postgre database should have postgres user"""
    ids = Db.objects.filter(
        type='S', type_db=Db.POSTGRESQL).values_list('id', flat=True)
    for id in ids:
        res = User.objects.filter(db_id=id, name='postgres').count()
        if res != 1:
            return ['Each server\'s Postgre db should have single "postgres" user!']
    return []


def validate_project_db1():
    """Each project database name should be unique"""
    names = Db.objects.filter(type='P').values_list('name', flat=True)
    if len(names) != len(set(names)):
        return ['Each project database name should be unique!']
    return []


def validate_project_db2():
    """Each project database should have single user"""
    ids = Db.objects.filter(type='P').values_list('id', flat=True)
    for id in ids:
        res = User.objects.filter(db_id=id).count()
        if res != 1:
            return ['Each project database should have single user!']
    return []


def validate_uwsgi():
    """Each django project should have unique uwsgi port"""
    ports = Project.objects.filter(
        type='DJ').values_list('uwsgi_port', flat=True)
    if len(ports) != len(set(ports)):
        return ['Each django project should have unique uwsgi port!']
    return []


def validate_server_ip():
    """Each server should have single "is_main" IP address"""
    ids = Server.objects.values_list('id', flat=True)
    for id in ids:
        res = Ip.objects.filter(server_id=id, is_main=True).count()
        if res != 1:
            return ['Each server should have single "is_main" IP address!']
    return []


def validate_project_dirs():
    """
        All project's directories should have "~" or "/" at the begin
        and "/" at the end.
    """
    errors = []
    projects = Project.objects.all()
    l = [
        'project_dir_server',
        'project_dir_local',
        'venv_dir_server',
        'venv_dir_local',
        'static_dir_server',
        'static_dir_local',
        'media_dir_server',
        'media_dir_local',
        'requirements_dir'
    ]

    for project in projects:
        for field in l:
            value = getattr(project, field)
            if not value:
                continue

            if value.startswith('~') or value.startswith('/'):
                pass
            else:
                message = 'Project: {}, {} should starts with \
                     "~" or "/"'.format(project.name, field)
                errors.append(message)

            if not value.endswith('/'):
                message = 'Project: {}, {} should ends with "/"'.format(
                    project.name, field)
                errors.append(message)
    return errors


def create_pattern(view, path, func_name):
    ptn = url(path, admin.site.admin_view(getattr(view, func_name)))
    return patterns('', ptn,)


def get_admin_urls(urls):
    def get_urls():
        my_urls = patterns('')

        my_models = (
            Server,
        )

        for MyModel in my_models:
            for path, view_name in MyModel.get_admin_urls():
                my_urls += create_pattern(views_admin, path, view_name)

        return my_urls + urls
    return get_urls

admin_urls = get_admin_urls(admin.site.get_urls())
admin.site.get_urls = admin_urls
