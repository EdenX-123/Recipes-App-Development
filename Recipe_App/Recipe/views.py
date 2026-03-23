from django.shortcuts import render, get_object_or_404
from .models import Recipe

def home_view(request):
    return render(request, 'Recipe/home.html')

def recipe(request,):

    return render(request, "Recipe/recipe.html")

def health_and_diet(request):
    
    return render(request, "Recipe/Health&Diet.html")

def holiday_recipes(request):

    return render(request, "Recipe/Holidays.html")

def Dessert(request):

    return render(request, "Recipe/Dessert.html")

def Drinks(request):

    return render(request, "Recipe/Drinks.html")

def Keto(request):

    return render(request, "Recipe/Keto.html")

def Vegetarian(request):

    return render(request, "Recipe/Vegetarian.html")

def MotherDay(request):

    return render(request, "Recipe/MotherDay.html")

def NewYear(request):
    
    return render(request, "Recipe/NewYear.html")

# recipe view
def breakfast(request):
    recipes = Recipe.objects.filter(category='breakfast')
    return render(request, "Recipe/breakfast.html",{
        'recipes': recipes
    })

def lunch(request):
    recipes = Recipe.objects.filter(category='lunch')
    return render(request, "Recipe/lunch.html", {
        'recipes': recipes
    })

def dinner(request):
    recipes = Recipe.objects.filter(category='dinner')
    return render(request, "Recipe/dinner.html", {
        'recipes': recipes
    })

# recipe detail view
def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    return render(request, "Recipe/recipe_detail.html", {
        'recipe': recipe
    })

# add edit and delete views
# add recipe view
from django.shortcuts import redirect
from .forms import RecipeForm
from django.contrib.auth.decorators import login_required

def add_recipe(request):

    if not request.user.is_authenticated:
        messages.error(request, "Please login first ⚠️")
        return redirect("/?login=true")

    if request.method == "POST":
        form = RecipeForm(request.POST, request.FILES)

        if request.method == "POST":
            form = RecipeForm(request.POST, request.FILES)

            if form.is_valid():

                if Recipe.objects.filter(
                    title=form.cleaned_data['title'],
                    author=request.user
                ).exists():
                    messages.warning(request, "Recipe already exists ⚠️")
                    return redirect("home")

            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()

            messages.success(request, "Recipe added successfully 🎉")
            return redirect('recipe_detail', recipe_id=recipe.id)
        
        else:
            messages.error(request, "Failed to add recipe ❌")

    else:
        form = RecipeForm()

    return render(request, 'Recipe/add_recipe.html', {
        'form': form
    })


# edit recipe view
def edit_recipe(request, recipe_id):

    recipe = get_object_or_404(Recipe, id=recipe_id)

    if recipe.author != request.user:
        messages.error(request, "You are not allowed to edit this recipe ❌")
        return redirect("home")
    
    form = RecipeForm(request.POST or None,
                      request.FILES or None,
                      instance=recipe)

    if form.is_valid():
        form.save()
        messages.success(request, "Recipe updated successfully ✅")
        return redirect('recipe_detail', recipe_id=recipe.id)

    return render(request, 'Recipe/edit_recipe.html', {
        'form': form
    })

# delete recipe view
def delete_recipe(request, recipe_id):

    recipe = get_object_or_404(Recipe, id=recipe_id)

    if recipe.author != request.user:
        messages.error(request, "You are not allowed to delete this recipe ❌")
        return redirect("home")

    recipe.delete()
    messages.success(request, "Recipe deleted successfully 🗑️")

    return redirect('home')


# user logining 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db import IntegrityError

# signup view
def signup(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")
        password1 = request.POST.get("password1")


        if len(username) < 4:
            messages.error(request,"Username must be at least 4 characters")
            return redirect("/?signup=true")

        if len(password) < 6:
            messages.error(request,"Password must be at least 6 characters")
            return redirect("/?signup=true")
        
        if password != password1:
            messages.error(request,"Passwords do not match ❌")
            return redirect("/?signup=true")

        try:
            user = User.objects.create_user(username=username, password=password)
        except IntegrityError:
            messages.error(request,"Username already exists ⚠️")
            return redirect("/?signup=true")
        
        login(request,user)
        messages.success(request,"Account created successfully 🎉")

        return redirect("/")

# user login view
def login_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        # print("AUTH RESULT:", user)
        # print("INPUT:", username)

        if user is not None:

            login(request, user)
            messages.success(request, f"Welcome back {username}! 👋")

            return redirect("home")
        
        else:
            messages.error(request, "Invalid username or password ❌")
            return redirect("/?login=true")

# logout view
def user_logout(request):
    logout(request)

    messages.success(request,"logged out successfully 👋")

    return redirect("/")

#search bar 
from django.db.models import Q

def search(request):
    query = request.GET.get("q")

    if query:
        recipes = Recipe.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(ingredients__icontains=query)
        )
    else:
        recipes = Recipe.objects.none()

    return render(request, "Recipe/search.html", {
        "recipes": recipes,
        "query": query
    })
