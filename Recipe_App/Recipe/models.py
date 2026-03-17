from django.db import models
from django.contrib.auth.models import User

class Recipe(models.Model):

    CATEGORY_CHOICES = [
        ('breakfast','Breakfast'),
        ('lunch','Lunch'),
        ('dinner','Dinner'),
    ]

    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField()
    ingredients = models.TextField()
    instructions = models.TextField()
    image = models.ImageField(upload_to='recipes/')


    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
