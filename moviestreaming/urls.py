from django.conf.urls import url
from django.urls import path
from django.conf.urls import include

from . import views

app_name = 'moviestreaming'

urlpatterns = [
    path('', views.start, name='start'),
    path('login', views.user_login, name='login'),
    path('logout', views.user_logout, name='logout'),
    path('adminPanel', views.admin_panel, name='home'),
    path('adminPanel/adduser', views.registration, name='registration'),
    path('adminPanel/users', views.show_users, name='show-users'),
    path('adminPanel/users/editusers', views.edit_users, name='edit_users'),
    path('adminPanel/users/saveeditusers', views.save_edit_users, name='save_edit_users'),
    path('adminPanel/addmovie', views.add_movie, name='addmovie'),
    path('adminPanel/showmovies', views.show_movies, name='show_movies'),
    path('adminPanel/showmovies/editmoviedetail', views.edit_movie_detail, name='edit_movie_detail'),
    path('adminPanel/showmovies/editmoviedetail/saveeditmoviedetails', views.save_edit_movie_details, name='save_edit_movie_detail'),
    path('home/showmovies/deletemovie', views.delete_movie, name='delete_movie'),
    path('home/shoeusers/deleteuser', views.delete_user, name='delete_user'),
    path('userpanel', views.user_panel, name='user_panel'),
    path('userpanel/rate', views.rate, name='rate'),








]
