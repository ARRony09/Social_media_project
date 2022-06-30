from django.urls import path
from . import views

app_name='App_login'

urlpatterns = [
    path('signup/',views.signup_form,name='signup'),
    path('login/',views.login_form,name='login'),
    path('logout/',views.login_form,name='logout'),
    path('edit/',views.edit_profile,name='edit'),
    path('user/',views.user_profile,name='user'),
    path('user_other/<username>/',views.user_other,name="user_other"),
    path('follow/<username>',views.follow,name="follow"),
    path('unfollow/<username>',views.unfollow,name="unfollow"),
]
