from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from .views import (IngredientViewSet, RecipeViewSet,
                    TagViewSet)
from users.views import UserViewSet


router_v1 = DefaultRouter()
router_v1.register(
    'ingredients', IngredientViewSet,
    basename='ingredient-processing',
)

router_v1.register('tags', TagViewSet)

router_v1.register(
    'recipes', RecipeViewSet,
    basename='recipe-processing',
)
router_v1.register(
    'users', UserViewSet,
    basename='user-processing',
)
urlpatterns = [
    path('', include(router_v1.urls)),
    re_path(r'auth/', include('djoser.urls.authtoken')),
]