from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from core.models import (Tag, Ingredient)
from recipe import serializers


class TagViewSet(viewsets.GenericViewSet,
                 mixins.ListModelMixin,
                 mixins.CreateModelMixin
                          ):
    """Mange tags in database"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer

    def get_queryset(self):
        """Return objects fot the current authentication user only"""
        return self.queryset.filter(user=self.request.user).order_by('-name')


    def perform_create(self, serializer):
        """Add property to serializer"""
        serializer.save(user=self.request.user)


class IngredientViewSet(mixins.ListModelMixin,
                        mixins.CreateModelMixin,
                        viewsets.GenericViewSet
                        ):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer

    def get_queryset(self):
        """Get object for authenticated user"""
        return self.queryset.filter(user=self.request.user)
   
    def perform_create(self, serializer):
        """Add user to the ingredient model"""
        serializer.save(user=self.request.user)

    
