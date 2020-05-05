from rest_framework.decorators import action
from rest_framework.response import Response

from rest_framework import viewsets, mixins, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from core.models import (Tag, Ingredient, Recipe)
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
   

class RecipeViewSet(viewsets.ModelViewSet):
    """Manage recipes"""
    serializer_class = serializers.RecipeSerializer
    queryset = Recipe.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Retrive recipe for authenticated user"""
        return self.queryset.filter(user=self.request.user)    
    
    def get_serializer_class(self):
        """Return a serializer to use for response"""
        if self.action == 'retrieve':
            return serializers.RecipeDetailSerializer
        elif self.action == 'upload_image':
           return serializers.RecipeImageSerializer
        
        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new recipe"""
        serializer.save(user=self.request.user)
    
    @action(methods=['POST'], detail=True, url_path='upload_image')
    def upload_image(self, request, pk=None):
        """Upload an image to recipe"""
        recipe = self.get_object()
        serializer = self.get_serializer(
            recipe,
            data=request.data
        )
        
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )