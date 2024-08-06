from django.db import models

class FruitVegetable(models.Model):
    name = models.CharField(max_length=100)
    vitamin_c = models.CharField(max_length=100, blank=True, null=True)
    fiber = models.CharField(max_length=100, blank=True, null=True)
    sugar = models.CharField(max_length=100, blank=True, null=True)
    calories = models.CharField(max_length=100, blank=True, null=True)
    protein = models.CharField(max_length=100, blank=True, null=True)
    fat = models.CharField(max_length=100, blank=True, null=True)
    carbohydrates = models.CharField(max_length=100, blank=True, null=True)
    potassium = models.CharField(max_length=100, blank=True, null=True)
    magnesium = models.CharField(max_length=100, blank=True, null=True)
    calcium = models.CharField(max_length=100, blank=True, null=True)
    iron = models.CharField(max_length=100, blank=True, null=True)
    vitamin_a = models.CharField(max_length=100, blank=True, null=True)
    vitamin_d = models.CharField(max_length=100, blank=True, null=True)
    vitamin_b6 = models.CharField(max_length=100, blank=True, null=True)
    vitamin_b12 = models.CharField(max_length=100, blank=True, null=True)
    # Add other nutrient fields as necessary

    def __str__(self):
        return self.name
