from django.urls import path

from . import views

urlpatterns = [
    
    path('', views.index, name='index'),
    path('info/<str:rdf_object>', views.info, name='info'),
    path('search/', views.search, name='search'),
]