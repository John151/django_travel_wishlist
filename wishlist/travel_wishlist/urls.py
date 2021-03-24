from django.urls import path
from . import views

# list of urls our app will recognize
# points requests made to homepage should be handled by place_list in views module
urlpatterns = [
    path('', views.place_list, name='place_list'),
    path('about', views.about, name='about')
]
