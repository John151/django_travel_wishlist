from django.shortcuts import render, redirect, get_object_or_404
from .models import Place
from .forms import NewPlaceForm, TripReviewForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages

# Create your views here.

@login_required
def place_list(request):

    if request.method == 'POST':
        # create a new place
        form = NewPlaceForm(request.POST)  # creating form from data in request
        place = form.save(commit=False)  # creating a model object form
        place.user = request.user
        if form.is_valid():  # database constraints validation
            place.save()  # saves place to database
            return redirect('place_list')  # reloads home page


    places = Place.objects.filter(user=request.user).filter(visited=False).order_by('name')
    new_place_form = NewPlaceForm()  # used to create HTML
    return render(request, 'travel_wishlist/wishlist.html', {'places': places, 'new_place_form': new_place_form})


def about(request):
    author = 'John'
    about = 'A website to create a list of places to visit'
    return render(request, 'travel_wishlist/about.html', {'author': author, 'about': about})

@login_required
def places_visited(request):
    visited = Place.objects.filter(user=request.user).filter(visited=True)
    return render(request, 'travel_wishlist/visited.html', {'visited': visited} )


# database query, getting object with pk == int passed by url
@login_required
def place_was_visited(request, place_pk):
    if request.method == 'POST':
        place = get_object_or_404(Place, pk=place_pk)
        if place.user == request.user:
            place.visited = True    
            place.save()
        else:
            return HttpResponseForbidden()

    return redirect('place_list')  # name of the path


@login_required
def place_details(request, place_pk):
    place = get_object_or_404(Place, pk=place_pk)
    
    # check if place belongs to current user
    if place.user != request.user:
        return HttpResponseForbidden()

    # check if GET request (show data + form) or POST request (update Place object)
    # if POST requerst, validate form data and update
    if request.method == 'POST':
        form = TripReviewForm(request.POST, request.FILES, instance=place)
        if form.is_valid():
            form.save()
            messages.info(request, 'Trip information updated!')
        else:
            messages.error(request, form.errors)

        return redirect('place_details', place_pk=place_pk)

    # if Get request show Place info and form
    # if place is visited, show form, if place is not visited no form
    else:
        if place.visited:
            review_form = TripReviewForm(instance=place)
            return render(request, 'travel_wishlist/place_detail.html', {'place': place, 'review_form': review_form})
        else:
            return render(request, 'travel_wishlist/place_detail.html', {'place': place})




@login_required
def delete_place(request, place_pk):
    place = get_object_or_404(Place, pk=place_pk)
    if place.user == request.user:
        place.delete()
        return redirect('place_list')
    else:
        return HttpResponseForbidden()