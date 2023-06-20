from django.contrib import admin
from django.db.models import Sum
from django.http import HttpResponse
from .views import Aisle, Unit, Recipe, Ingredient


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')


@admin.register(Aisle)
class AisleAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')


class IngredientInline(admin.TabularInline):
    model = Ingredient
    extra = 0


@admin.action(description="Generate shopping list")
def generate_shopping_list(modeladmin, request, queryset):
    ingredients = Ingredient.objects \
        .filter(recipe__in=queryset) \
        .values('name', 'unit__name', 'aisle__name') \
        .annotate(total_quantity=Sum('quantity')) \
        .order_by('aisle__name', 'name')
    
    response = ""
    for i in ingredients:
        if i['aisle__name']:
            response += f"({i['aisle__name']}) "
        response += f"{i['total_quantity']} {i['unit__name']} {i['name']}\n"

    return HttpResponse(response, content_type='text/plain')


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = [IngredientInline]
    actions = [generate_shopping_list]
    list_display = ('name', 'ingredient_count')

    def ingredient_count(self, obj):
        return obj.ingredient_set.all().count()
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.prefetch_related('ingredient_set')