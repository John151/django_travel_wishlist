from django.test import TestCase
from django.urls import reverse

from .models import Place

# Create your tests here.

# checks what template was used, tests with empty database
class TestHomePage(TestCase):

    def test_home_page_shows_empty_list_message_for_empty_database(self):
        home_page_url = reverse('place_list')
        response = self.client.get(home_page_url)
        self.assertTemplateUsed(response, 'travel_wishlist/wishlist.html')
        self.assertContains(response, 'You have no places in your wishlist.')

class TestWishList(TestCase):
    # django will assume .json format, look first in fixtures directory
    fixtures = ['test_places']

    def test_wishlist_contains_not_visited_places(self):
        response = self.client.get(reverse('place_list'))
        self.assertTemplateUsed(response, 'travel_wishlist/wishlist.html')
        self.assertContains(response, 'Tokyo')
        self.assertContains(response, 'New York')
        self.assertNotContains(response, 'San Francisco')
        self.assertNotContains(response, 'Moab')

class TestVisitedPage(TestCase):
    def test_visited_shows_empty_list_message_for_empty_database(self):
        visited_page = reverse('places_visited')
        response = self.client.get(visited_page)
        self.assertTemplateUsed(response, 'travel_wishlist/visited.html')
        self.assertContains(response, 'You have not visited any places yet.')

class TestVisitedList(TestCase):
    fixtures = ['test_places']

    def test_only_visited_places_displayed(self):
        response = self.client.get(reverse('places_visited'))
        self.assertTemplateUsed(response, 'travel_wishlist/visited.html')
        self.assertContains(response, 'San Francisco')
        self.assertContains(response, 'Moab')
        self.assertNotContains(response, 'Tokyo')
        self.assertNotContains(response, 'New York')

class TestAddNewPlace(TestCase):

    def test_add_new_unvisited_place(self):
        add_place_url = reverse('place_list')
        new_place_data = {'name': 'Tokyo', 'visited': False}
        response = self.client.post(add_place_url, new_place_data, follow=True)

        self.assertTemplateUsed(response, 'travel_wishlist/wishlist.html')
        # this response object has a value context, dictionary
        response_places = response.context['places']
        self.assertEqual(1, len(response_places)) # check only 1 place added
        tokyo_from_response = response_places[0]

        tokyo_from_database = Place.objects.get(name='Tokyo', visited=False)
        # making sure the value the view sent to the template is the same as what ended up in the database
        self.assertEqual(tokyo_from_database, tokyo_from_response)

class TestVisitPlace(TestCase):
    fixtures = ['test_places']

    def test_visit_place(self):
        visit_place_url = reverse('place_was_visited', args=(2,))
        response = self.client.post(visit_place_url, follow=True)
        # using a redirect, we want to make sure it used the correct template
        self.assertTemplateUsed(response, 'travel_wishlist/wishlist.html')

        self.assertNotContains(response, 'New York')
        # Tokyo should still be there
        self.assertContains(response, 'Tokyo')

        new_york = Place.objects.get(pk=2)
        self.assertTrue(new_york.visited)

        #making sure we get a 404 response when a place doesn't exist
    def test_non_existent_place(self):
        visit_nonexistent_place_url = reverse('place_was_visited', args=(12356, ))
        response = self.client.post(visit_nonexistent_place_url, follow=True)
        self.assertEqual(404, response.status_code)