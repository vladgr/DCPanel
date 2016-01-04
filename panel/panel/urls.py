from django.conf.urls import include, url
from django.contrib import admin

from rest_framework import routers
from api import views as v

router = routers.DefaultRouter()
router.register(r'conf', v.ConfViewSet)
router.register(r'country', v.CountryViewSet)
router.register(r'db', v.DbViewSet)
router.register(r'install', v.InstallViewSet)
router.register(r'ip', v.IpViewSet)
router.register(r'project', v.ProjectViewSet)
router.register(r'provider', v.ProviderViewSet)
router.register(r'server', v.ServerViewSet)
router.register(r'user', v.UserViewSet)


admin.site.site_header = 'Control Panel'

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(router.urls)),

    url(r'^api/postfix/(?P<server_id>\d+)/$', v.PostfixItem.as_view()),
    url(r'^api/project-list/(?P<type>.+)/$', v.ProjectListByType.as_view()),
    url(r'^api/project-by-name/(?P<name>.+)/$', v.ProjectByName.as_view()),
    url(r'^api/server-conf/(?P<server_id>\d+)/$', v.ServerConfList.as_view()),
    url(
        r'^api/server-conf/(?P<server_id>\d+)/(?P<item>.+)/(?P<filename>.+)/$',
        v.ServerConfItem.as_view()
    ),

    url(
        r'^api/project-conf/(?P<project_id>\d+)/(?P<item>.+)/$',
        v.ProjectConfListByItem.as_view()
    ),

    # settings
    url(r'^api/local-linux-username/$', v.LocalLinuxUsername.as_view()),
    url(r'^api/local-bash-dir/$', v.LocalBashDir.as_view()),
    url(r'^api/confirmation-password/$', v.ConfirmationPassword.as_view()),
    url(r'^api/server-control-script/$', v.ServerControlScript.as_view()),

    url(r'^$', v.home)
]
