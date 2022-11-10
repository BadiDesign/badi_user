"""badi_users_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views
from badi_users_project import settings

# handler404 = 'badi_utils.views.my_custom_page_not_found_view'
urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', include('badi_user.ui.urls')),
                  path('', include('badi_ticket.urls')),
                  path('', include('badi_wallet.ui.urls')),
                  path('api/v1/', include('badi_user.api.routers')),
                  path('api/v1/', include('badi_ticket.routers')),
                  path('api/v1/', include('badi_wallet.api.routers')),
                  path('api/v1/', include('badi_visit.api.routers')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
