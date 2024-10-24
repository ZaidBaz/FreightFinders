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
    path('search-locations/', views.search_locations, name='search_locations'),
    path('multi-capacity-types/', views.multi_capacity_type, name = 'multi_capacity_types'),
    path('search-dates', views.search_dates, name = 'search_dates')
]
