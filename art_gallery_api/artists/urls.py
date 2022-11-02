
from django.urls import re_path
from artists import views

urlpatterns = [
    re_path(r'api/artists$', views.ListArtists.as_view()),
    re_path(r'api/artists/(?P<pk>[0-9]+)$', views.ListArtistDetail.as_view()),
]