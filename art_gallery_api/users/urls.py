from django.urls import re_path
from users import views

urlpatterns = [
    re_path(r'api/users$', views.ListUsers.as_view()),
    re_path(r'api/users/(?P<pk>[0-9]+)$', views.ListUserDetail.as_view()),
]