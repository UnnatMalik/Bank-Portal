
from django.contrib import admin
from django.urls import path , include
from django.conf import settings
from django.conf.urls.static import static
from bank import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('bank.urls'))
]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

handler404 = 'bank.views.handler404'
