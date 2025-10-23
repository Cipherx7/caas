"""
URL configuration for commhub project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('landing.urls')),  # Landing page at root
    path('communities/', include('communities.urls')),  # Directory page
    path('accounts/', include('accounts.urls')),  # Login/Signup
    path('sponsors/', __import__('communities.views').views.sponsors_directory, name='sponsors_directory'),
    path('sponsors/<int:pk>/', __import__('communities.views').views.sponsor_detail, name='sponsor_detail'),
    path('dashboard/leader/', __import__('communities.views_dashboard').views_dashboard.leader_dashboard, name='leader_dashboard'),
    path('dashboard/leader/community/edit/', __import__('communities.views_dashboard').views_dashboard.edit_community, name='community_edit'),
    path('dashboard/leader/community/<int:pk>/edit/', __import__('communities.views_dashboard').views_dashboard.edit_community_pk, name='community_edit_pk'),
    path('dashboard/leader/community/<int:pk>/manage/', __import__('communities.views_dashboard').views_dashboard.manage_community_pk, name='community_manage_pk'),
    path('dashboard/leader/community/<int:pk>/events/', __import__('communities.views_dashboard').views_dashboard.events_list_create, name='events_list_create'),
    path('dashboard/leader/community/<int:pk>/events/<int:event_id>/edit/', __import__('communities.views_dashboard').views_dashboard.event_edit, name='event_edit'),
    path('dashboard/leader/community/<int:pk>/events/<int:event_id>/delete/', __import__('communities.views_dashboard').views_dashboard.event_delete, name='event_delete'),
    path('dashboard/leader/community/<int:pk>/sponsorships/', __import__('communities.views_dashboard').views_dashboard.sponsorships_list_create, name='sponsorships_list_create'),
    path('dashboard/leader/community/<int:pk>/sponsorships/<int:sponsorship_id>/edit/', __import__('communities.views_dashboard').views_dashboard.sponsorship_edit, name='sponsorship_edit'),
    path('dashboard/leader/community/<int:pk>/sponsorships/<int:sponsorship_id>/delete/', __import__('communities.views_dashboard').views_dashboard.sponsorship_delete, name='sponsorship_delete'),
    path('dashboard/leader/community/<int:pk>/sponsors/', __import__('communities.views_dashboard').views_dashboard.sponsors_list_create, name='sponsors_list_create'),
    path('dashboard/leader/community/<int:pk>/sponsors/<int:sponsor_id>/edit/', __import__('communities.views_dashboard').views_dashboard.sponsor_edit, name='sponsor_edit'),
    path('dashboard/leader/community/<int:pk>/sponsors/<int:sponsor_id>/delete/', __import__('communities.views_dashboard').views_dashboard.sponsor_delete, name='sponsor_delete'),
    path('communities/new/', __import__('communities.views_dashboard').views_dashboard.new_community, name='community_new'),
]
