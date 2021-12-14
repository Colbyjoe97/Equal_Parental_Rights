from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^sign$', views.sign),
    url(r'^admin/register$', views.admin),
    url(r'^register$', views.register_admin),
    url(r'^login$', views.login),
    url(r'^admin/page$', views.admin_page),
]