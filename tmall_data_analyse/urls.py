"""tmall_data_analyse URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from vis import views as visual

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', visual.order_vis),
    url(r'^order/$',visual.order_vis),
    url(r'^fee/$',visual.fee_vis),
    url(r'^inv/$',visual.inv_vis),
    url(r'^inv/mon/$',visual.inv_mon_vis),
    url(r'^load/$',visual.jump_to_load),
    url(r'^upload/$',visual.upload),
    url(r'^testd3/$',visual.testd3),
]