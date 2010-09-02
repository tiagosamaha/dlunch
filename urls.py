from django.contrib import admin
from django.conf.urls.defaults import *
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/dlunch/relatorio/$', 'dlunch.admin_views.relatorio', name="relatorio"),    
    (r'^admin/(.*)$', admin.site.root),
    (r"^media/(.*)$", 'django.views.static.serve',\
            {'document_root': settings.MEDIA_ROOT}),
    (r'^api/', include('api.urls')),
)
