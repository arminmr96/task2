from django.db import models

# Create your models here.
class TitanicPassenger(models.Model):
    passenger_id = models.CharField(max_length=20, primary_key=True)
    survived = models.IntegerField(choices=[
        (0, "Drowned"),
        (1, "Survived"),
    ]) 
    pclass = models.IntegerField(choices=[
        (1, "First Class"),
        (2, "Second Class"),
        (3, "Third Class"),
    ])
    name = models.CharField(max_length=255)
    sex = models.CharField(max_length=10, choices=[
        ('male', 'Male'),
        ('female', 'Female'),
    ])
    age = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    sibsp = models.IntegerField(null=True, blank=True)  
    parch = models.IntegerField(null=True, blank=True)  
    ticket = models.CharField(max_length=50, blank=True) 
    fare = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    cabin = models.CharField(max_length=20, blank=True, null=True) 
    embarked = models.CharField(max_length=1, choices=[
        ('C', 'Cherbourg'),
        ('S', 'Southampton'),
        ('Q', 'Queenstown'),
    ], blank=True, null=True) 
    

    def __str__(self):
        return self.name 