from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from core.models import Ingredient
from recipe.serializers import IngredientSerializer


INGREDIENTS_URL= reverse('recipe:ingredient-list')


class PublicIngredientsApiTests(TestCase):
    """Test the publicly avalible api ingerient"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required for retriving Igreidt"""
        res = self.client.get(INGREDIENTS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientsApiTests(TestCase):
    """Test the authorized user ingerient API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'saeed@gmail.com',
            'pass123'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_ingredient_list(self):
        """Test retrieving ingredient"""
        Ingredient.objects.create(user = self.user, name = 'Vegan')
        Ingredient.objects.create(user = self.user, name = 'Dessert')

        res = self.client.get(INGREDIENTS_URL)
        ingredient = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(ingredient , many= True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_ingredients_limited_to_user(self):
        """Test that ingredients return is for authenticated user"""
        user2 = get_user_model().objects.create_user(
                'test@gmail.com',
                'pass123'
        )
        Ingredient.objects.create(user = user2, name = 'Fruity')
        ingredient = Ingredient.objects.create(user = self.user, name = 'Comfort Food')

        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], ingredient.name)