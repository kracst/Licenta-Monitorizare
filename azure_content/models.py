from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    name = models.CharField(max_length=500, unique=True)
    description = models.CharField(max_length=500,blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    edited_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name 
    
class SensorData(models.Model):

    temperature = models.FloatField()
    humidity = models.FloatField()
    luminosity = models.FloatField()
   # ph = models.FloatField()  # Optional field for pH
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.temperature}°C, {self.humidity}%, {self.luminosity}%, {self.timestamp}"