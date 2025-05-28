from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Q, F

from users.models import User


class Ingredient(models.Model):
    """Ingredients for recipes"""
    name = models.TextField(blank=True)
    measurement_unit = models.TextField(blank=True)

    class Meta:
        db_table = 'ingredients'

    def __str__(self):
        return self.name


class Tag(models.Model):
    """Tags for recipes with predefined choices."""
    GREEN = '09db4f'
    ORANGE = 'fa6a02'
    PURPLE = 'b813d1'
    COLOR_TAG = [
        (GREEN, 'Green'),
        (ORANGE, 'Orange'),
        (PURPLE, 'Purple')
    ]
    name = models.CharField(
        verbose_name='Tag name',
        max_length=200, unique=True,
        help_text='Tag Name')
    color = models.CharField(
        verbose_name='Color in HEX',
        max_length=7, unique=True,
        default=GREEN,
        choices=COLOR_TAG,
        help_text='Choose color')
    slug = models.SlugField(
        verbose_name='Unique slug',
        max_length=200, unique=True,
        help_text='Unique slug')

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = 'Tags'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """
    Model for recipes.
    An author cannot create more than one recipe with the same name.
    """
    author = models.ForeignKey(
        User,
        verbose_name='Recipe author',
        on_delete=models.CASCADE,
        help_text='Recipe author')
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientRecipe',
        verbose_name='Ingredient')
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Tag name',
        help_text='Choose tag')
    text = models.TextField(
        verbose_name='Recipe description',
        help_text='Describe the recipe')
    name = models.CharField(
        verbose_name='Recipe name',
        max_length=200,
        help_text='Recipe name',
        db_index=True)
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Cooking time',
        validators=[MinValueValidator(1, 'Minimum cooking time')],
        help_text='Minimum cooking time')
    image = models.ImageField(
        verbose_name='Image',
        upload_to='media/',
        help_text='Recipe image')
    pub_date = models.DateTimeField(
        verbose_name='Publication date',
        auto_now_add=True)

    class Meta:
        ordering = ['-id']
        default_related_name = 'recipe'
        verbose_name = 'Recipe'
        verbose_name_plural = 'Recipes'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'author'],
                name='unique_recipe')]


class IngredientRecipe(models.Model):
    """
    Ingredients for a recipe.
    Intermediate model between:
      Recipe and Ingredient
    """
    recipe = models.ForeignKey(
        Recipe,
        related_name='recipe_ingredients',
        verbose_name='Recipe name',
        on_delete=models.CASCADE,
        help_text='Choose recipe')
    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name='Ingredient',
        on_delete=models.CASCADE,
        help_text='Choose ingredient')
    amount = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1, 'Minimum ingredient count is 1')],
        verbose_name='Quantity',
        help_text='Ingredient quantity')

    class Meta:
        verbose_name = 'Composition'
        verbose_name_plural = 'Recipe composition'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_ingredients')]

    def __str__(self):
        return f'{self.ingredient} {self.amount}'


class ShoppingCart(models.Model):
    """
    User's shopping list.
    Unique constraints on:
      author, recipe.
    """
    author = models.ForeignKey(
        User,
        related_name='shopping_cart',
        on_delete=models.CASCADE,
        verbose_name='User')
    recipe = models.ForeignKey(
        Recipe,
        related_name='shopping_cart',
        verbose_name='Recipe to cook',
        on_delete=models.CASCADE,
        help_text='Select a recipe to cook')

    class Meta:
        verbose_name = 'Shopping list'
        verbose_name_plural = 'Shopping lists'
        constraints = [models.UniqueConstraint(
            fields=['author', 'recipe'],
            name='unique_cart')]

    def __str__(self):
        return f'{self.recipe}'


class Favorite(models.Model):
    """
    User's favorites list.
    Unique constraints on:
      author, recipe.
    """
    author = models.ForeignKey(
        User,
        related_name='favorite',
        on_delete=models.CASCADE,
        verbose_name='Recipe author')
    recipe = models.ForeignKey(
        Recipe,
        related_name='favorite',
        on_delete=models.CASCADE,
        verbose_name='Recipes')

    class Meta:
        verbose_name = 'Favorite recipes'
        verbose_name_plural = 'Favorite recipes'
        constraints = [models.UniqueConstraint(
            fields=['author', 'recipe'],
            name='unique_favorite')]

    def __str__(self):
        return f'{self.recipe}'


class Follow(models.Model):
    """
    Subscriptions to recipe authors.
    Unique constraints on:
      user, author.
    """
    user = models.ForeignKey(
        User,
        verbose_name='User',
        related_name='follower',
        on_delete=models.CASCADE,
        help_text='Current user')
    author = models.ForeignKey(
        User,
        verbose_name='Subscription',
        related_name='followed',
        on_delete=models.CASCADE,
        help_text='Subscribe to recipe author(s)')

    class Meta:
        verbose_name = 'My subscriptions'
        verbose_name_plural = 'My subscriptions'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_following'),
            models.CheckConstraint(
                check=~Q(user=F('author')),
                name='no_self_following')]

    def __str__(self):
        return f'User {self.user} is subscribed to {self.author}'
