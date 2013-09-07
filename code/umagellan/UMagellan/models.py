from django.db import models
from django.contrib.auth.models import User

# represents a class
class Class(models.Model):
    department = models.ForeignKey(User)
    course_number = models.IntegerField()
    section = models.IntegerField()
    building_code = models.TextField(max_length=3) 
    room_number = models.IntegerField()
    
# the route that the user will take from start_location to end_location
class Route(models.Model):
    start_location = models.ForeignKey(Class, related_name='class_start_location')
    end_location = models.ForeignKey(Class, related_name='class_end_location')
    user = models.ForeignKey(User)
    
# represents a point of interest
class POI(models.Model):
    name = models.TextField()
    x_coord = models.DecimalField(max_digits=20, decimal_places=12)
    y_coord = models.DecimalField(max_digits=20, decimal_places=12)