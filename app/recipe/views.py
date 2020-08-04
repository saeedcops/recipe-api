from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from core.models import Tag, Ingredient
from recipe import serializers


class BaseRecipeViewSet(viewsets.GenericViewSet,
                 mixins.ListModelMixin,
                 mixins.CreateModelMixin):
    """Base ViewSet Recipe in the database"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Return object for the current authenticated user only"""
        return self.queryset.filter(user = self.request.user).order_by('-name')

    def perform_create(self, serializer):
        """Create a new  tag"""
        serializer.save(user = self.request.user)


class TagViewSet(BaseRecipeViewSet):
    """Mange tags in the database"""
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer
        

class IngredientViewSet(BaseRecipeViewSet):
    """Mange Ingredient in the database"""

    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer