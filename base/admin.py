from django.contrib import admin
from .models import Shape

# Register your models here.
admin.site.register(Shape) # Register the User model with the admin site
def admin_register_shape():
    """
    Registers the Shape model with the Django admin site.
    """
    admin.site.register(Shape)
