from django.db import models

# Create your models here.
class Shape(models.Model):
    """
    Represents a shape object with a name, timestamp, color, and shape type.
    """

    SHAPE_CHOICES = [
        ('circle', 'Circle'),
        ('rectangle', 'Rectangle'),
        ('triangle', 'Triangle'),
    ] # Create a list of choices for the shape field

    name = models.CharField(max_length=100) # Add a name field with a maximum length of 100 characters
    timestamp = models.DateTimeField(auto_now_add=True) # Add a timestamp field that automatically adds the current date and time
    color = models.CharField(max_length=7) # Add a color field with a maximum length of 7 characters
    shape = models.CharField(max_length=10, choices=SHAPE_CHOICES)  # Add a shape field with a maximum length of 10 characters and limited choices
    
    def __str__(self):
        return self.name