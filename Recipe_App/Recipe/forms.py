from django import forms
from .models import Recipe, Review
class RecipeForm(forms.ModelForm):

    class Meta:
        model = Recipe
        fields = [
            "title",
            "category",
            "description",
            "ingredients",
            "instructions",
            "image"
        ]

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']