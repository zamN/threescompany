from django.db import models
from django.contrib.auth.models import User

# represents a class
class Class(models.Model):
    department = models.ForeignKey(User)
    course_number = models.IntegerField(max_value=9999)
    section = models.IntegerField(max_value=9999)
    building_code = models.TextField(max_length=3) 
    room_number = models.IntegerField(max_value=9999)
    
# the route that the user will take from start_location to end_location
class Route(models.Model):
    start_location = models.ForeignKey(Class)
    end_location = models.ForeignKey(Class)
    user = models.ForeignKey(User)
    
# represents a point of interest
class POI(models.Model):
    name = models.TextField()
    x_coord = models.DecimalField()
    y_coord = models.DecimalField()