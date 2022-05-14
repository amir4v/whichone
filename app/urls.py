from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('votes', views.votes, name='votes'),
    path('avote/<int:id>', views.avote, name='avote'),
    path('avote-result/<int:id>', views.avote_result, name='avote-result'),
    path('rather/<int:avote>/<int:choosed>/<int:refused>', views.rather, name='rather'),
]