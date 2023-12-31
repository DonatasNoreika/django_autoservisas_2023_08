from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('automobiliai/', views.automobiliai, name='automobiliai'),
    path('automobiliai/<int:auto_id>', views.automobilis, name='automobilis'),
    path('search/', views.search, name='search'),
    path('register/', views.register, name='register'),
    path("profile/", views.profile, name="profile"),
    path('myuzsakymai/', views.MyUzsakymasListView.as_view(), name='my_uzsakymai'),
    path('uzsakymai/', views.UzsakymasListView.as_view(), name='uzsakymai'),
    path('uzsakymai/<int:pk>', views.UzsakymasDetailView.as_view(), name='uzsakymas'),
    path("uzsakymai/new/", views.UzsakymasCreateView.as_view(), name='uzsakymas_new'),
    path('uzsakymai/<int:pk>/update/', views.UzsakymasUpdateView.as_view(), name="uzsakymas_update"),
    path('uzsakymai/<int:pk>/delete/', views.UzsakymasDeleteView.as_view(), name="uzsakymas_delete"),
    path('uzsakymai/<int:pk>/newline/', views.UzsakymoEiluteCreateView.as_view(), name='uzsakymoeilute_new'),
    path('uzsakymai/<int:uzsakymas_id>/eilute_istrinti/<int:pk>', views.UzsakymoEiluteDeleteView.as_view(), name='uzsakymoeilute_delete'),
    path('uzsakymai/<int:uzsakymas_id>/eilute_redaguoti/<int:pk>', views.UzsakymoEiluteUpdateView.as_view(), name='uzsakymoeilute_edit'),
]