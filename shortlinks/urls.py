from django.urls import path
from . import views

urlpatterns = [
    path('links/', views.ShortLinkListCreateView.as_view(), name='shortlink-list-create'),
    path('links/<str:slug>/', views.ShortLinkDetailView.as_view(), name='shortlink-detail'),
]