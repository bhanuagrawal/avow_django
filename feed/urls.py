from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^image/$', views.upload_photo),
    url(r'^home$', views.user_posts),
]