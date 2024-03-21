from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='Home'),
    path('about', views.about, name='About'),
    path('sect', views.sect, name='Sect'),

    path('<int:article_id>', views.deteil, name='deteil'), 
    path('<int:article_id>/leave_comment/', views.leave_comment, name='leave_comment'), 
    path('profile', views.profile, name='Profile')
]