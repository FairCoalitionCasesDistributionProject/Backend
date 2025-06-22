import os
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import status
import pyrebase
import json
import re
from .division import Division
from .util import *
from .inputcheck import isvalidinput


# Load Firebase config from environment variables
config = {
    "apiKey": os.getenv('FIREBASE_API_KEY'),
    "authDomain": os.getenv('FIREBASE_AUTH_DOMAIN'),
    "projectId": os.getenv('FIREBASE_PROJECT_ID'),
    "storageBucket": os.getenv('FIREBASE_STORAGE_BUCKET'),
    "messagingSenderId": os.getenv('FIREBASE_MESSAGING_SENDER_ID'),
    "appId": os.getenv('FIREBASE_APP_ID'),
    "databaseURL": os.getenv('FIREBASE_DATABASE_URL'),
}

# Validate Firebase config
if not all(config.values()):
    raise ValueError("Missing Firebase configuration environment variables")

firebase = pyrebase.initialize_app(config)
authe = firebase.auth()
database = firebase.database()


def sanitize_key(key):
    """Sanitize database key to prevent injection attacks"""
    if not isinstance(key, str):
        return None
    
    # Remove any potentially dangerous characters
    sanitized = re.sub(r'[^a-zA-Z0-9._-]', '', key)
    
    # Prevent directory traversal
    if '..' in sanitized or '/' in sanitized:
        return None
    
    return sanitized


def run_algo(json_data, type):
    try:
        # Enhanced input validation
        if (
            not isinstance(json_data, dict)
            or not isvalidinput(json_data)
            or not isinstance(json_data.get("key"), str)
        ):
            return Response(
                {"error": "Invalid input format"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Sanitize the key
        sanitized_key = sanitize_key(json_data["key"])
        if not sanitized_key:
            return Response(
                {"error": "Invalid key format"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Limit data size to prevent abuse
        if len(str(json_data)) > 10000:  # 10KB limit
            return Response(
                {"error": "Input data too large"}, 
                status=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE
            )
        
        # Store data in Firebase
        if (
            "type" in json_data.keys()
            and isinstance(json_data["type"], int)
            and json_data["type"] == 0
        ):
            database.child(sanitized_key.replace(".", "/")).set(
                json.dumps(json_data)
            )
        else:
            database.child(sanitized_key.replace(".", "/")).set(
                str(json_data["preferences"])
            )

        prefs = json_data["preferences"]
        div = Division(number_of_items=json_data["items"])
        div.add_parties([(i, json_data["mandates"][i]) for i in range(len(prefs))])

        for i in range(len(prefs)):
            div.set_party_preferences(i, normalize(prefs[i]))
        allocation = transpose(bundle_to_matrix(div.divide()))
        
        if type == 0:
            return Response(str(allocation).replace("[", "{").replace("]", "}"))
        else:
            return Response(
                {
                    "allocation": allocation,
                    "rounded_allocation": round_allocation(allocation),
                }
            )

    except Exception as e:
        # Log the error (in production, use proper logging)
        print(f"Error in run_algo: {str(e)}")
        return Response(
            {"error": "Internal server error"}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(["POST"])
@permission_classes([AllowAny])  # Temporarily allow anonymous access
def AlgoResponseView(request):
    try:
        if (
            isinstance(request.data, dict)
            and "_content" in request.data.keys()
            and isinstance(request.data["_content"], str)
        ):
            return run_algo(json.loads(request.data["_content"]), 0)
        else:
            return run_algo(request.data, 0)
    except json.JSONDecodeError:
        return Response(
            {"error": "Invalid JSON format"}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        return Response(
            {"error": "Request processing error"}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(["POST"])
@permission_classes([AllowAny])  # Temporarily allow anonymous access
def AlgoResponseTestView(request):
    try:
        if (
            isinstance(request.data, dict)
            and "_content" in request.data.keys()
            and isinstance(request.data["_content"], str)
        ):
            return run_algo(json.loads(request.data["_content"]), 1)
        else:
            return run_algo(request.data, 1)
    except json.JSONDecodeError:
        return Response(
            {"error": "Invalid JSON format"}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        return Response(
            {"error": "Request processing error"}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(["POST"])
@permission_classes([AllowAny])  # Temporarily allow anonymous access
def ReturnSaveView(request):
    try:
        if not isinstance(request.data.get("key"), str):
            return Response(
                {"error": "Invalid key"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Sanitize the key
        sanitized_key = sanitize_key(request.data["key"])
        if not sanitized_key:
            return Response(
                {"error": "Invalid key format"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        data = database.child(sanitized_key.replace(".", "/")).get().val()
        if not isinstance(data, str):
            return Response(
                {"error": "Data not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        return Response(data)
    except Exception as e:
        return Response(
            {"error": "Data retrieval error"}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )












































































