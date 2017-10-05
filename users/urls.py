from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^home/', views.hello, name='hello'),
    url(r'^api/$', views.user_list),
    url(r'^login/$', views.user_login),
    url(r'^update$', views.update_user),
    url(r'^image/$', views.upload_file),
    url(r'^search$', views.search_user),
    url(r'^follow/$', views.follow),
    url(r'^followmany$', views.followMany),
    url(r'^unfollow/$', views.unfollow),
    url(r'^unfollowmany$', views.unfollowMany),
    url(r'^device/$', views.add_user_android_device),
    url(r'^removedevice/$', views.remove_user_android_device),
    url(r'^details$', views.user_profile),
    url(r'^followers$', views.followers),
    url(r'^following$', views.following),
    url(r'^registered$', views.registeredUsers),

]
