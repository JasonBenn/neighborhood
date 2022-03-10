from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('analytics', views.analytics),
    path('ratings', views.create_rating, name='create_rating'),
]
