from rest_framework import generics, status
from rest_framework.response import Response
# from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny
from .models import User,Item
from .serializers import UserSerializer,ItemSerializer
from rest_framework.decorators import api_view
import jwt
from datetime import datetime,timedelta
import pytz
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed,NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework import HTTP_HEADER_ENCODING, exceptions
from inventory.oauth2 import create_access_token, verify_access_token
from django.core.cache import cache
from django.http import Http404
import logging








class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": serializer.data,
            "message": "User registered successfully"
        }, status=status.HTTP_201_CREATED)
        
        




class UserLoginView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    def create(self, request, *args, **kwargs):
        data = request.data
        try:
            username = data.get("username")
            password = data.get("password")
            if not username or not password:
                raise AuthenticationFailed("Username and password are required")
            user = User.objects.filter(username=username).first()
            if not user:
                raise AuthenticationFailed("Invalid Credentials")
            if user.password!=password:
                raise AuthenticationFailed("Invalid Credentials")
            token_data = {"email": user.email, "username": user.username,"id": user.id}
            token = create_access_token(token_data)  # Adjust this to your actual token generation logic
            return Response({"token": token, "user_id": user.id, "username": user.username}, status=status.HTTP_200_OK)
        except AuthenticationFailed as e:
            return Response({"detail": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({"detail": "An error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
class ItemCreationView(generics.CreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [AllowAny]
    def create(self, request, *args, **kwargs):
        item_data = request.data
        description = item_data.get("description")
        token = None
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if auth_header is None:
            raise AuthenticationFailed("Authorization header not found")
        if auth_header:
            try:
                token_type, token = auth_header.split()  
                if token_type.lower() != 'bearer':
                    token = None  
            except ValueError:
                token = None  
        print("Retrieved Token:", token)
        user=verify_access_token(token)
        print(user)
        if user is None:
            raise AuthenticationFailed("Invalid token")
        valid=User.objects.filter(id=user["id"]).first()
        if valid is None:
            raise AuthenticationFailed("Invalid token")
        existing_item = Item.objects.filter(name=item_data.get("name")).first()
        if existing_item:
            return Response({
                "item": ItemSerializer(existing_item).data,
                "message": "Item already exists"
            }, status=status.HTTP_400_BAD_REQUEST)
        data=request.data.copy()
        data["added_by"]=user["id"]
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({
            "item": serializer.data,
            "message": "Item created successfully"
        }, status=status.HTTP_201_CREATED)
        
        
class ItemDetailView(generics.RetrieveAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [AllowAny]

    # def get(self, request, *args, **kwargs):
    #     item_id = self.kwargs.get('pk')
    #     token = None
    #     auth_header = request.META.get('HTTP_AUTHORIZATION')
    #     if auth_header is None:
    #         raise AuthenticationFailed("Authorization header not found")
        
    #     if auth_header:
    #         try:
    #             token_type, token = auth_header.split()  
    #             if token_type.lower() != 'bearer':
    #                 token = None  
    #         except ValueError:
    #             token = None  

    #     user = verify_access_token(token)
    #     if user is None:
    #         raise AuthenticationFailed("Invalid token")
        
    #     valid = User.objects.filter(id=user["id"]).first()
    #     if valid is None:
    #         raise AuthenticationFailed("Invalid token")


        # cache_key = f'item_detail_{item_id}'
        # item_data = cache.get(cache_key)

        # if item_data is None:
        #     try:
        #         item = self.get_object()
        #         item_data = ItemSerializer(item).data
        #         cache.set(cache_key, item_data, timeout=60*15)  
        #     except Item.DoesNotExist:
        #         return Response({
        #             "message": "Item not found"
        #         }, status=status.HTTP_404_NOT_FOUND)
        # else:
        #     print("Cache hit for item:", item_id)

        # return Response({
        #     "item": item_data,  
        #     "message": "Item retrieved successfully"
        # }, status=status.HTTP_200_OK)



    def get(self, request, *args, **kwargs):
        item_id = self.kwargs.get('pk')
        token = None
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        
        # Check for authorization header
        if auth_header is None:
            raise AuthenticationFailed("Authorization header not found")

        if auth_header:
            try:
                token_type, token = auth_header.split()  
                if token_type.lower() != 'bearer':
                    token = None  
            except ValueError:
                token = None  

        user = verify_access_token(token)
        if user is None:
            raise AuthenticationFailed("Invalid token")
        
        valid = User.objects.filter(id=user["id"]).first()
        if valid is None:
            raise AuthenticationFailed("Invalid token")

        # Retrieve the item from the database
        try:
            item = self.get_object()  # This will use the queryset defined in the class
            item_data = ItemSerializer(item).data  # Serialize the item data
        except Item.DoesNotExist:
            return Response({
                "message": "Item not found"
            }, status=status.HTTP_404_NOT_FOUND)

        # Optionally use caching
        # cache_key = f'item_detail_{item_id}'
        # item_data = cache.get(cache_key)

        # if item_data is None:
        #     # Set item data in cache
        #     cache.set(cache_key, item_data, timeout=60*15)
        # else:
        #     print("Cache hit for item:", item_id)

        return Response({
            "item": item_data,  
            "message": "Item retrieved successfully"
        }, status=status.HTTP_200_OK)

            
            
            
class ItemUpdateView(generics.UpdateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [AllowAny]  

    def update(self, request, *args, **kwargs):
        item = self.get_object()  
        
        token = None
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if auth_header is None:
            raise AuthenticationFailed("Authorization header not found")

        if auth_header:
            try:
                token_type, token = auth_header.split()  
                if token_type.lower() != 'bearer':
                    token = None  
            except ValueError:
                token = None  

        user = verify_access_token(token)
        if user is None:
            raise AuthenticationFailed("Invalid token")
        valid=User.objects.filter(id=user["id"]).first()
        if valid is None:
            raise AuthenticationFailed("Invalid token")

        item_data = request.data.copy()  
        item_data["added_by"] = user["id"]  

        
        serializer = self.get_serializer(item, data=item_data, partial=True)  
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response({
            "item": serializer.data,
            "message": "Item updated successfully"
        }, status=status.HTTP_200_OK)
        
        
# class ItemDeleteView(generics.DestroyAPIView):
#     queryset = Item.objects.all()
#     permission_classes = [AllowAny]  

#     def delete(self, request, *args, **kwargs):
#         item = self.get_object()  
        
#         token = None
#         auth_header = request.META.get('HTTP_AUTHORIZATION')
#         if auth_header is None:
#             raise AuthenticationFailed("Authorization header not found")

#         if auth_header:
#             try:
#                 token_type, token = auth_header.split()  
#                 if token_type.lower() != 'bearer':
#                     token = None  
#             except ValueError:
#                 token = None  

#         user = verify_access_token(token)
#         if user is None:
#             raise AuthenticationFailed("Invalid token")
#         valid=User.objects.filter(id=user["id"]).first()
#         if valid is None:
#             raise AuthenticationFailed("Invalid token")

#         self.perform_destroy(item)

#         return Response({
#             "message": "Item deleted successfully"
#         }, status=status.HTTP_204_NO_CONTENT)
#             return Response({
#                 "message": "Item not found"
#             }, status=status.HTTP_404_NOT_FOUND)




class ItemDeleteView(generics.DestroyAPIView):
    queryset = Item.objects.all()
    permission_classes = [AllowAny]  

    def delete(self, request, *args, **kwargs):
        token = None
        auth_header = request.META.get('HTTP_AUTHORIZATION')

        # Check for authorization header
        if auth_header is None:
            raise AuthenticationFailed("Authorization header not found")

        # Extract token from header
        try:
            token_type, token = auth_header.split()  
            if token_type.lower() != 'bearer':
                raise AuthenticationFailed("Authorization must be a Bearer token")
        except ValueError:
            raise AuthenticationFailed("Invalid token format")

        # Verify the access token
        user = verify_access_token(token)
        if user is None:
            raise AuthenticationFailed("Invalid token")

        valid = User.objects.filter(id=user["id"]).first()
        if valid is None:
            raise AuthenticationFailed("Invalid token")

        # Attempt to retrieve the item
        try:
            item = self.get_object()  # This will raise a 404 if the item does not exist
        except Http404:
            return Response({
                "message": "Item not found"
            }, status=status.HTTP_404_NOT_FOUND)

        # Perform the delete operation
        self.perform_destroy(item)

        return Response({
            "message": "Item deleted successfully"
        }, status=status.HTTP_204_NO_CONTENT)