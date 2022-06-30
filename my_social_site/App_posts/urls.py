from django.urls import path,include
from .import views

app_name='App_post'

urlpatterns = [
    path('',views.home,name='home'),
    path('like/<pk>/',views.like,name='like'),
    path('unlike/<pk>',views.unlike,name='unlike'),
    path('comment/<pk>/',views.comment,name='comment'),
]
