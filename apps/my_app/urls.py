from django.conf.urls import url, handler404
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^sign$', views.sign, name="sign_form"),
    url(r'^admin/register$', views.admin),
    url(r'^register$', views.register_admin, name="register_admin"),
    url(r'^login$', views.login, name="login"),
    url(r'^admin/page$', views.admin_page, name="admin_page"),
    url(r'^', views.bad_request),
]