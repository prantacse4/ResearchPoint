from django.contrib import admin
from django.urls import path,re_path, include
from django.conf import settings
from django.conf.urls.static import static
from Discussions import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Discussions.urls')),
    path('', include('Accounts.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT )

wrongurls = [
    re_path('.*/', views.wrong, name='wrong'),
]
urlpatterns += wrongurls