import api.bm as models
import api.serializers as sers
import logging

from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.generic import View

from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import generics

logger = logging.getLogger('app')


def home(request):
    return HttpResponse('Control Panel')


class ConfViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Conf.objects.all()

    def list(self, request):
        serializer = sers.ConfListSerializer(self.queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        obj = get_object_or_404(models.Conf, pk=pk)
        serializer = sers.ConfDetailSerializer(obj)
        return Response(serializer.data)


class CountryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Country.objects.all()
    serializer_class = sers.CountrySerializer


class DbViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Db.objects.all()

    def list(self, request):
        serializer = sers.DbListSerializer(self.queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        obj = get_object_or_404(models.Db, pk=pk)
        serializer = sers.DbDetailSerializer(obj)
        return Response(serializer.data)


class InstallViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Install.objects.all()
    serializer_class = sers.InstallSerializer


class IpViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Ip.objects.all()
    serializer_class = sers.IpSerializer


class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Project.objects.all()

    def list(self, request):
        serializer = sers.ProjectListSerializer(self.queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        obj = get_object_or_404(models.Project, pk=pk)
        serializer = sers.ProjectDetailSerializer(obj)
        return Response(serializer.data)


class ProviderViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Provider.objects.all()
    serializer_class = sers.ProviderSerializer


class ServerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Server.objects.all()

    def list(self, request):
        serializer = sers.ServerListSerializer(self.queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Retrieves by id or code"""
        filter = {'id': pk} if pk.isdigit() else {'code': pk}

        obj = get_object_or_404(models.Server, **filter)
        serializer = sers.ServerDetailSerializer(obj)
        return Response(serializer.data)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.User.objects.all()

    def list(self, request):
        serializer = sers.UserListSerializer(self.queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        obj = get_object_or_404(models.User, pk=pk)
        serializer = sers.UserDetailSerializer(obj)
        return Response(serializer.data)


class ProjectListByType(generics.ListAPIView):
    serializer_class = sers.ProjectDetailSerializer

    def get_queryset(self):
        """Returns projects(detail) for particular type"""
        print(self.kwargs)
        return models.Project.objects.filter(**self.kwargs)


class ProjectByName(generics.RetrieveAPIView):
    serializer_class = sers.ProjectDetailSerializer

    def get_object(self):
        obj = get_object_or_404(models.Project, **self.kwargs)
        return obj


class ProjectConfListByItem(generics.ListAPIView):
    serializer_class = sers.ConfDetailSerializer

    def get_queryset(self):
        """Returns Confs for particular project by item"""
        return models.Conf.objects.filter(**self.kwargs)


class ServerConfList(generics.ListAPIView):
    serializer_class = sers.ConfListSerializer

    def get_queryset(self):
        """Returns Confs for particular server"""
        return models.Conf.objects.filter(**self.kwargs)


class ServerConfItem(generics.RetrieveAPIView):
    serializer_class = sers.ConfDetailSerializer

    def get_object(self):
        obj = get_object_or_404(models.Conf, **self.kwargs)
        return obj


class PostfixItem(generics.RetrieveAPIView):
    serializer_class = sers.PostfixSerializer

    def get_object(self):
        obj = get_object_or_404(models.Postfix, **self.kwargs)
        return obj


class SettingsBase(View):
    code = ''

    def get_obj(self):
        try:
            obj = models.Setting.objects.get(code=self.code)
        except models.Setting.DoesNotExist:
            raise Exception('Settings code "{}" not found.'.format(self.code))
        return obj

    def get(self, request):
        obj = self.get_obj()
        return JsonResponse({'value': obj.value})


class LocalLinuxUsername(SettingsBase):
    """Returns local machine's username."""
    code = '001'


class LocalBashDir(SettingsBase):
    """Returns path to directory with bash scripts."""
    code = '002'


class ConfirmationPassword(SettingsBase):
    """Returns confirmation password for important operations"""
    code = '003'


class ServerControlScript(SettingsBase):
    """Returns path to server control script"""
    code = '004'
