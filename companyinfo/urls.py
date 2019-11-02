from django.urls import path

from . import views

urlpatterns = [
    
    path('', views.index, name='index'),
    path('<str:rdf_object>/info/', views.info, name='info'),
    path('search/', views.search, name='search'),
]