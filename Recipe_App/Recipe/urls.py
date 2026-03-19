from django.urls import path
from . import views


urlpatterns = [
    path('', views.home_view, name='home'),
    path('home/', views.home_view, name='home'),
    path('recipe/', views.recipe, name='recipe'),

    path('health-diet/', views.health_and_diet, name='health_and_diet'),
    path('holidays/', views.holiday_recipes, name='holiday_recipes'),

    # recipe urls
    path('breakfast/',views.breakfast,name='breakfast'),
    path('lunch/',views.lunch,name='lunch'),
    path('dinner/',views.dinner,name='dinner'),
    # recipe detail url
    path('recipe/<int:recipe_id>/',views.recipe_detail,name='recipe_detail'),
    # add edit and delete urls
    path('add/',views.add_recipe,name='add_recipe'),
    path('edit/<int:recipe_id>/',views.edit_recipe,name='edit_recipe'),
    path('delete/<int:recipe_id>/',views.delete_recipe,name='delete_recipe'),
    # login and logout urls
    path("signup/", views.signup, name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.user_logout, name="logout"),
    #search bar
    path("search/", views.search, name="search"),
]