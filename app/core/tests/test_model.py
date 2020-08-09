from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models

def sample_user(email = 'saeed@gmail.com', password = 'pass123'):
    """Create sample user"""
    return get_user_model().objects.create_user(email, password)


    
class ModelTests(TestCase):

    def test_create_user_with_email_sucsseful(self):
        """Test create with email succseful"""
        email = "saeed@gmail.com"
        password = "password123"
        user = get_user_model().objects.create_user(
                                                email=email,
                                                password=password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_normalized(self):
        """Test new email if normalized"""
        email = 'saeed@GMAIL.COM'
        user = get_user_model().objects.create_user(
                                                email=email,
                                                password="passw123")

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test user with invalid email address"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, "passw0988")

    def test_new_superuser(self):
        """Test if the user is superuser"""
        user = get_user_model().objects.create_superuser("saeed@gmail.com", "pass123")
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        """Test tag string represintaion"""
        tag = models.Tag.objects.create(
                    user = sample_user(),
                    name = 'Vegas'
        )

        self.assertEqual(str(tag), tag.name)


    def test_ingredient_str(self):
        """Test ingredient string represintaion"""
        ingredient = models.Ingredient.objects.create(
                    user = sample_user(),
                    name = 'Cucumber'
        )

        self.assertEqual(str(ingredient), ingredient.name)

    def test_recipe_str(self):
        """Test recipe string represintaion"""
        recipe = models.Recipe.objects.create(
                    user = sample_user(),
                    title = 'Steak and mashrom souce',
                    time_minutes = 5,
                    price = 5.00
        )

        self.assertEqual(str(recipe), recipe.title)