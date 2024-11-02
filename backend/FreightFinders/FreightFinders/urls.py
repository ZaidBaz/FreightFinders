"""
URL configuration for FreightFinders project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path
from backendapp import views


urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('filter-loads/', views.filter_loads, name = 'filter-loads'),

    #PC MILER APIs
    path('single-search/', views.single_search_view, name='single_search'),
    path('geocode/', views.geocode_search_view, name='geocode_search'),
    path('reverse-geocode/', views.reverse_geocode_view, name='reverse_geocode'),
    path('radius-search/', views.radius_search_view, name='radius_search'),
    
]
