from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='Home'),
    path('about', views.about, name='About'),
    path('sect', views.sect, name='Sect'),

    path('<int:article_id>/', views.detail, name='detail'), 
    path('<int:article_id>/leave_comment/', views.leave_comment, name='leave_comment'),
    path('edit_comment/<int:comment_id>/', views.edit_comment, name='edit_comment'),
    path('delete_comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),

    path('profile', views.profile, name='profile'),
    path('add_respan/', views.add_respan, name='add_respan'),
    path('remove_respan/', views.remove_respan, name='remove_respan'),
]