from django.urls import path
from . import views

urlpatterns = [
    path('<str:slug>/', views.redirect_view, name='redirect'),
]