from django.urls import re_path
from videos import views

urlpatterns = [
    re_path(r'api/videos$', views.ListVideos.as_view()),
    re_path(r'api/videos/(?P<pk>[0-9]+)$', views.ListVideoDetail.as_view()),
    re_path(r'api/videos/published$', views.ListPublishedVideos.as_view())
]