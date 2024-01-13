from django.core import serializers
from django.forms import model_to_dict
from django.shortcuts import render
from django.views import View
from django.http import JsonResponse

from base.consumers import ShapesConsumer
from .models import Shape
import json
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.core import serializers


class ShapesView(View):
    """
    A view class for handling requests related to shapes.

    Methods:
    - get: Handles GET requests to retrieve shape data.
    - post: Handles POST requests to create a new shape.
    - put: Handles PUT requests to update an existing shape.
    - delete: Handles DELETE requests to delete a shape.
    - updateConsumer: Sends shape data to a consumer for real-time updates.
    """

    def get(self, request):
        """
        Handles GET requests to retrieve shape data.

        Parameters:
        - request: The HTTP request object.

        Returns:
        - JsonResponse: A JSON response containing the retrieved shape data.
        """
        try:
            if request.GET.get("id"): # Check if the request contains an "id" query parameter
                id = request.GET.get("id") # Get the value of the "id" query parameter
                item = Shape.objects.filter(id=id).values().first() # Retrieve the shape data from the database

                if item:
                    return JsonResponse({"message": "GET request received", "data": item}) # Return a success response
                else:
                    return JsonResponse({"error": "Shape not found"}, status=404) # Return an error response if shape not found
            else:
                items = Shape.objects.all().values() # Retrieve all shape data from the database
                items_data = list(items) # Convert the QuerySet to a list
                return JsonResponse({"message": "GET request received", "data": items_data}) # Return a success response
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500) # Return an error response for any other exceptions

    def post(self, request):
        """
        Handles POST requests to create a new shape.

        Parameters:
        - request: The HTTP request object.

        Returns:
        - JsonResponse: A JSON response indicating the success of the request.
        """
        try:
            data = json.loads(request.body) # Convert the JSON string to a Python dictionary
            name = data.get("name") # Get the value of the "name" key
            color = data.get("color")   # Get the value of the "color" key
            shape = data.get("shape")  # Get the value of the "shape" key

            if not name or not color or not shape: # Check if any of the required fields are missing
                return JsonResponse({"error": "Missing required fields"}, status=400) # Return an error response

            shape = Shape(name=name, color=color, shape=shape) # Create a new Shape object
            shape.save() # Save the object to the database

            self.updateConsumer(data=model_to_dict(shape), type="shapes.add") # Send the new shape data to the consumer
            return JsonResponse({"message": "POST request received", "success": True}) # Return a success response
        except json.JSONDecodeError: 
            return JsonResponse({"error": "Invalid JSON format"}, status=400) # Return an error response
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500) # Return an error response

    def put(self, request):
        """
        Handles PUT requests to update an existing shape.

        Parameters:
        - request: The HTTP request object.

        Returns:
        - JsonResponse: A JSON response indicating the success of the request.
        """
        try:
            data = json.loads(request.body) # Convert the JSON string to a Python dictionary
            id = data.get("id") # Get the value of the "id" key
            name = data.get("name") # Get the value of the "name" key
            color = data.get("color") # Get the value of the "color" key
            shape = data.get("shape") # Get the value of the "shape" key

            if not id or not name or not color or not shape: # Check if any of the required fields are missing
                return JsonResponse({"error": "Missing required fields"}, status=400) # Return an error response

            shapeObject = Shape.objects.get(id=id) # Retrieve the shape object from the database
            shapeObject.name = name # Update the shape object
            shapeObject.color = color # Update the shape object
            shapeObject.shape = shape # Update the shape object
            shapeObject.save() # Save the updated shape object to the database

            self.updateConsumer(data=model_to_dict(shapeObject), type="shapes.update") # Send the updated shape data to the consumer
            return JsonResponse({"message": "PUT request received", "success": True}) # Return a success response
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400) # Return an error response
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500) # Return an error response

    def delete(self, request):
        """
        Handles DELETE requests to delete a shape.

        Parameters:
        - request: The HTTP request object.

        Returns:
        - JsonResponse: A JSON response indicating the success of the request.
        """
        try:
            data = json.loads(request.body) # Convert the JSON string to a Python dictionary
            id = data.get("id") # Get the value of the "id" key
            if not id: # Check if the "id" key is missing
                return JsonResponse({"error": "Missing required fields"}, status=400)   # Return an error response

            shape = Shape.objects.get(id=id) # Retrieve the shape object from the database
            shape.delete() # Delete the shape object from the database
            self.updateConsumer(data=id, type="shapes.delete") # Send the deleted shape data to the consumer
            return JsonResponse({"message": "DELETE request received", "success": True}) # Return a success response
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400) # Return an error response
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500) # Return an error response

    def updateConsumer(self, data, type):
        """
        Sends shape data to a consumer for real-time updates.

        Parameters:
        - data: The shape data to be sent.
        - type: The type of update to be performed.

        Returns:
        - None
        """
        channel_layer = get_channel_layer() # Retrieve the channel layer
        async_to_sync(channel_layer.group_send)( 
            "shapes",
            {
                "type": type,
                "data": data
            }
        ) # Send the data to the consumer


shapes_view = ShapesView.as_view()  # Instantiate the view class
