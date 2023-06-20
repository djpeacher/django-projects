from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.shortcuts import render, redirect
from django.urls import path
from django.views.generic import TemplateView
from neapolitan.views import CRUDView
from .models import Aisle, Unit, Recipe, Ingredient


class UnitView(LoginRequiredMixin, CRUDView):
    model = Unit
    fields = ["name"]

    def get_queryset(self):
        return Unit.objects.filter(user=self.request.user)
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return redirect("unit-list")


class AisleView(LoginRequiredMixin, CRUDView):
    model = Aisle
    fields = ["name"]

    def get_queryset(self):
        return Aisle.objects.filter(user=self.request.user)
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return redirect("aisle-list")


class RecipeView(LoginRequiredMixin, CRUDView):
    model = Recipe
    fields = ["name", "note"]

    def get_queryset(self):
        return Recipe.objects.filter(user=self.request.user)
    
    def list(self, request, *args, **kwargs):
        self.fields = ["name"]
        return super().list(request, *args, **kwargs)
    
    def detail(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.request.session['recipe'] = self.object.id
        return redirect("ingredient-list")
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return redirect("recipe-list")


class IngredientView(LoginRequiredMixin, CRUDView):
    model = Ingredient
    fields = ["name", "quantity", "unit", "aisle"]

    def get_queryset(self):
        recipe, user = self.request.session['recipe'], self.request.user
        return Ingredient.objects.filter(recipe=recipe, recipe__user=user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recipe'] = Recipe.objects.get(id=self.request.session['recipe'])
        return context
    
    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.fields['unit'].queryset = Unit.objects.filter(user=self.request.user)
        form.fields['aisle'].queryset = Aisle.objects.filter(user=self.request.user)
        return form
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.recipe_id = self.request.session['recipe']
        self.object.save()
        return redirect("ingredient-list")


@login_required
def shopping_list(request):
    # https://docs.djangoproject.com/en/4.2/topics/db/aggregation/#values
    return render(request, "recipes/shopping_list.html", {
        'ingredients': Ingredient.objects \
            .filter(recipe__user=request.user) \
            .filter(recipe__in=request.GET.getlist("id")) \
            .values('name', 'unit__name', 'aisle__name') \
            .annotate(total_quantity=Sum('quantity')) \
            .order_by('aisle__name', 'name')}
    )


urlpatterns = [
    path('', TemplateView.as_view(template_name="recipes/index.html")),
    path('shopping-list/', shopping_list, name="shopping-list"),
    *RecipeView.get_urls(),
    *IngredientView.get_urls(),
    *AisleView.get_urls(),
    *UnitView.get_urls(),
]