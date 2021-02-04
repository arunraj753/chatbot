from django.urls import path,include
from .views import home
from . import views
urlpatterns = [

    path('',views.web,name='home'),
    path('chat',views.chat,name='chat'),
    path('update',views.update,name='update')


]