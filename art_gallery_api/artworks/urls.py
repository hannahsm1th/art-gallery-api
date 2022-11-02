from django.urls import re_path
from artworks import views

urlpatterns = [
    re_path(r'api/artworks$', views.ListArtworks.as_view()),
    re_path(r'api/artworks/(?P<pk>[0-9]+)$', views.ListArtworkDetail.as_view()),
    re_path(r'api/artworks/displayed$', views.ListDisplayedArtworks.as_view())
]