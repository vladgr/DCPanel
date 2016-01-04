import api.bm as models
import re

from django.contrib import messages
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext


@transaction.atomic
def copy_config(request):
    tpl = 'admin/api/custom/copy_config.html'
    servers = models.Server.objects.all()

    if request.method == 'POST':
        sfrom = int(request.POST['server_from'])
        sto = int(request.POST['server_to'])

        if sfrom == 0:
            message = 'Server "from" hasn\'t been chosen.'
            messages.error(request, message)
        elif sto == 0:
            message = 'Server "to" hasn\'t been chosen.'
            messages.error(request, message)
        elif sfrom == sto:
            message = 'Server "from" and server "to" should be different.'
            messages.error(request, message)
        else:
            count = 0
            objs = models.Conf.objects.filter(server_id=sfrom)
            for obj in objs:
                dic = {
                    'server_id': sto,
                    'filename': obj.filename,
                    'type': models.Conf.SERVER,
                    'item': obj.item
                }
                if not models.Conf.objects.filter(**dic).exists():
                    dic['data'] = obj.data
                    conf = models.Conf(**dic)
                    conf.save()
                    count += 1
            message = '{:d} configs have been copied.'.format(count)
            messages.success(request, message)

    return render_to_response(
        tpl, locals(), context_instance=RequestContext(request))


def check_server_configs(request, server_id):
    """Checks server's configuration.

    When server has some installs it should have
    particular configs for these installs.
    """

    server = get_object_or_404(models.Server, id=server_id)

    installs = models.Install.objects.filter(server_id=server.id)
    for i in installs:
        if i.item in ['mysql', 'postgresql']:
            if i.item == 'mysql':
                type_db = 'M'
            else:
                type_db = 'P'

            message_01 = '{}: {}: Db not found'.format(server.code, i.item)
            message_02 = '{}: {}: Db version not correct (It should be x.x)'\
                .format(server.code, i.item)
            message_03 = '{}: {}: root user not found'\
                .format(server.code, i.item)

            try:
                db = models.Db.objects.get(
                    server_id=server.id, type='S', type_db=type_db)
                if not re.match('\d\.\d$', db.version):
                    messages.error(request, message_02)
                models.User.objects.get(type='db', db_id=db.id, name='root')
            except models.Db.DoesNotExist:
                messages.error(request, message_01)
                messages.error(request, message_03)
            except models.User.DoesNotExist:
                messages.error(request, message_03)

        for filename in i.required_files():
            dic = dict(server_id=server.id, item=i.item, filename=filename)
            if not models.Conf.objects.filter(**dic).exists():
                message = '{}: {}: {} not found'\
                    .format(server.code, i.item, filename)
                messages.error(request, message)

    storage = messages.get_messages(request)
    if len(storage) == 0:
        messages.success(request, "Server is ready for install.")

    return HttpResponseRedirect('/admin/api/server/{}/'.format(server_id))
