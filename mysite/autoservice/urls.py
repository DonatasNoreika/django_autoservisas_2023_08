from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('automobiliai/', views.automobiliai, name='automobiliai'),
    path('automobiliai/<int:auto_id>', views.automobilis, name='automobilis'),
    path('uzsakymai/', views.UzsakymasListView.as_view(), name='uzsakymai'),
    path('uzsakymai/<int:pk>', views.UzsakymasDetailView.as_view(), name='uzsakymas'),
    path('search/', views.search, name='search'),
    path('myuzsakymai/', views.MyUzsakymasListView.as_view(), name='my_uzsakymai'),
    path('register/', views.register, name='register'),
]