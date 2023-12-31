"""
URL configuration for ocp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
import main.views as views


urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    
    path('stagiaires/', views.stagiaire_list, name='stagiaire_list'),
    path('stagiaires/<int:pk>/', views.stagiaire_detail, name='stagiaire_detail'),
    path('stagiaires/add/', views.stagiaire_add, name='stagiaire_add'),
    path('stagiaires/<int:pk>/edit/', views.stagiaire_edit, name='stagiaire_edit'),
    path('stagiaires/<int:pk>/delete/', views.stagiaire_delete, name='stagiaire_delete'),
    path('encadrants/', views.encadrant_list, name='encadrant_list'),
    path('encadrants/<int:encad_id>/', views.encadrant_detail, name='encadrant_detail'),
    path('encadrants/<int:encad_id>/delete/', views.encadrant_delete, name='encadrant_delete'),
    path('encadrants/add/', views.encadrant_add, name='encadrant_add'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
