from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('analytics', views.analytics),
    path('nose', views.nose),
    path('thanks', views.thanks),
    path('ratings', views.create_rating, name='create_rating'),
]
