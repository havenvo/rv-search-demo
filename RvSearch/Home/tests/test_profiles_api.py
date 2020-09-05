from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient

from Core.models import Profile, ServiceType, \
    ServiceRate, Country, Address, PetType

SEARCH_PROFILE_URL = reverse('search-alternative')


def create_test_user(email):
    return get_user_model().objects.create(email=email, password='Test@123')


def create_test_country():
    return Country.objects.create(
        iso_code='VN',
        name='Vietnam'
    )


def create_test_address(country):
    return Address.objects.create(
        address_line1='Address Line 1',
        postal_code='550000',
        city='City',
        state_province='StateX',
        country=country
    )


class SearchProfileTests(TestCase):

    def setUp(self):
        self.boarding = ServiceType.objects.create(display_name='Boarding', short_code='boarding')
        self.drop_in = ServiceType.objects.create(display_name='Drop-In Visits', short_code='drop_in')
        self.country = create_test_country()
        self.address = create_test_address(self.country)
        self.user = create_test_user('user@example.com')
        self.another_user = create_test_user('another@example.com')
        self.cat = PetType.objects.create(short_code='cat', display_name='Cat')
        self.dog = PetType.objects.create(short_code='dog', display_name='Dog')
        self.client = APIClient()

    def test_query_profile_response_correct(self):
        # a profile with boarding service, price = 15, our expectation
        profile_boarding_a = Profile.objects.create(
            user=self.user,
            first_name='A',
            last_name='A',
            title='A title',
            description='A description',
            reviews_count=100,
            rating_average=4.5,
            address=self.address
        )
        ServiceRate.objects.create(
            service_type=self.boarding,
            profile=profile_boarding_a,
            price=15
        )

        # b profile provides only drop-in
        profile_drop_in_b = Profile.objects.create(
            user=create_test_user('userb@example.com'),
            first_name='B',
            last_name='B',
            title='B title',
            description='B description',
            reviews_count=10,
            rating_average=5,
            address=create_test_address(self.country)
        )
        ServiceRate.objects.create(
            service_type=self.drop_in,
            profile=profile_drop_in_b,
            price=15
        )

        # a2 profile with boarding service but price = 100
        profile_boarding_a_2 = Profile.objects.create(
            user=create_test_user('usera2@example.com'),
            first_name='A2',
            last_name='A2',
            title='A2 title',
            description='A2 description',
            reviews_count=10,
            rating_average=5,
            address=create_test_address(self.country)
        )
        ServiceRate.objects.create(
            service_type=self.boarding,
            profile=profile_boarding_a_2,
            price=100
        )

        query = {
            'accept': 'json',
            'service_type': 'boarding',
            'min_price': 0,
            'max_price': 80
        }
        res = self.client.get(SEARCH_PROFILE_URL, query)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertContains(res, profile_boarding_a.title)
        self.assertNotContains(res, profile_drop_in_b.title)  # Not in due to not boarding service type
        self.assertNotContains(res, profile_boarding_a_2.title)  # Not in due to the price

    def test_assign_pet_types_should_fine(self):
        cat = PetType.objects.create(

        )

        profile = Profile.objects.create(
            user=self.user,
            first_name='A',
            last_name='A',
            title='A title',
            description='A description',
            reviews_count=100,
            rating_average=4.5,
            address=self.address
        )

        profile.pet_types.add(cat)
        profile.refresh_from_db()

        pet_types = profile.pet_types.all()
        self.assertTrue(pet_types.count(), 1)
        self.assertIn(cat, pet_types.all())

    def test_filter_pet_type(self):
        profile_dog = Profile.objects.create(
            user=self.user,
            first_name='A',
            last_name='A',
            title='A title',
            description='A description',
            address=self.address
        )
        profile_dog.pet_types.add(self.dog)

        profile_cat = Profile.objects.create(
            user=self.another_user,
            first_name='B',
            last_name='B',
            title='B title',
            description='B description',
            address=create_test_address(self.country)
        )
        profile_cat.pet_types.add(self.cat)

        query = {
            'accept': 'json',
            'pet_type': 'dog,',
        }
        res = self.client.get(SEARCH_PROFILE_URL, query)
        self.assertContains(res, profile_dog.title)
        self.assertNotContains(res, profile_cat.title)

    def test_filter_pet_num(self):
        profile_1 = Profile.objects.create(
            user=self.user,
            first_name='A',
            last_name='A',
            title='A title',
            description='A description',
            address=self.address,
            pet_num=1
        )

        profile_2 = Profile.objects.create(
            user=self.another_user,
            first_name='B',
            last_name='B',
            title='B title',
            description='B description',
            address=create_test_address(self.country),
            pet_num=2
        )

        query = {
            'pet_num': 2
        }
        res = self.client.get(SEARCH_PROFILE_URL, query)

        self.assertContains(res, profile_2.title)
        self.assertNotContains(res, profile_1.title)
