from django.urls import path
from . import views

urlpatterns = [
    path("", views.directory, name="communities_directory"),
    path("<int:pk>/", views.detail, name="community_detail"),
]
