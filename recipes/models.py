from django.db import models
from django.conf import settings

# HACK: There must be a better way to do this, but this returns __str__ output
# from the foreign key object instead of the raw id. 
class CustomForeignKey(models.ForeignKey):
    def value_to_string(self, obj):
        return str(getattr(obj, obj._meta.get_field(self.attname).name))
    
class Unit(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=16)
    
    def __str__(self):
        return self.name

class Aisle(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    
    def __str__(self):
        return self.name

class Recipe(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    note = models.TextField(blank=True)

    def __str__(self):
        return self.name
    
class Ingredient(models.Model):
    name = models.CharField(max_length=128)
    quantity = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    unit = CustomForeignKey(Unit, on_delete=models.SET_NULL, blank=True, null=True)
    aisle = CustomForeignKey(Aisle, on_delete=models.SET_NULL, blank=True, null=True)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    
    def __str__(self):
        ingredient = ""
        if self.aisle:
            ingredient += f"({self.aisle}) "
        ingredient += f"{self.quantity} {self.unit} {self.name}"
        return ingredient