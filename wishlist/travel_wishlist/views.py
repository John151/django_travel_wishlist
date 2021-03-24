from django.shortcuts import render, redirect
from .models import Place
from .forms import NewPlaceForm
# Create your views here.


def place_list(request):

    if request.method == 'POST':
        # create a new place
        form = NewPlaceForm(request.POST)  # creating form from data in request
        place = form.save()  # creating a model object form
        if form.is_valid():  # database constraints validation
            place.save()  # saves place to database
            return redirect('place_list')  # reloads home page


    places = Place.objects.filter(visited=False).order_by('name')
    new_place_form = NewPlaceForm()  # used to create HTML
    return render(request, 'travel_wishlist/wishlist.html', {'places': places, 'new_place_form': new_place_form})

def about(request):
    author = 'John'
    about = 'A website to create a list of places to visit'
    return render(request, 'travel_wishlist/about.html', {'author': author, 'about': about})