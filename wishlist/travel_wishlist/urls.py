from django.urls import path
from . import views

# list of urls our app will recognize
# name is used for url reversing
# points requests made to homepage should be handled by place_list in views module
urlpatterns = [
    path('', views.place_list, name='place_list'),
    path('about', views.about, name='about'),
    path('place/<int:place_pk>/was_visited', views.place_was_visited, name='place_was_visited'),
    path('visited', views.places_visited, name='places_visited'),
    path('place/<int:place_pk>', views.place_details, name='place_details'),
    path('place/<int:place_pk>/delete', views.delete_place, name='delete_place')
]
