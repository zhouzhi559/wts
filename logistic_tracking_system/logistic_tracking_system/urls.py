"""logistic_tracking_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from django.urls import include, re_path
from django.views.generic.base import TemplateView
from django.views.static import serve
from logistic_tracking_system import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns = [
    path('admin/', admin.site.urls),
    # path('logistic/', admin.site.urls),
    path("logistic/", include('lts.urls')),
    path('', TemplateView.as_view(template_name='index.html')),
    path(r"media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT})
]
urlpatterns += staticfiles_urlpatterns()