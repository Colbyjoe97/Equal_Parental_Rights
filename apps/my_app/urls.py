from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^sign$', views.sign),
    url(r'^admin/register$', views.admin),
    url(r'^admin', views.register_admin),
]