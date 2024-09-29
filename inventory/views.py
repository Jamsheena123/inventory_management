from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny
from .models import CustomUser
from .serializers import CustomUserSerializer, CustomTokenObtainPairSerializer

# User Registration View
class UserRegistrationView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": serializer.data,
            "message": "User registered successfully"
        }, status=status.HTTP_201_CREATED)

# User Login View using JWT
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [AllowAny]

class ItemViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request):
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            item = serializer.save()
            logger.info(f"Item created: {item.name}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        item = cache.get(f'item_{pk}')
        if not item:
            try:
                item = Item.objects.get(pk=pk)
                cache.set(f'item_{pk}', item, timeout=60*15)  # Cache for 15 minutes
            except Item.DoesNotExist:
                logger.error(f"Item not found: {pk}")
                return Response({"detail": "Item not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ItemSerializer(item)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            item = Item.objects.get(pk=pk)
            serializer = ItemSerializer(item, data=request.data)
            if serializer.is_valid():
                serializer.save()
                logger.info(f"Item updated: {item.name}")
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Item.DoesNotExist:
            logger.error(f"Item not found for update: {pk}")
            return Response({"detail": "Item not found."}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        try:
            item = Item.objects.get(pk=pk)
            item.delete()
            logger.info(f"Item deleted: {item.name}")
            return Response({"detail": "Item deleted."}, status=status.HTTP_204_NO_CONTENT)
        except Item.DoesNotExist:
            logger.error(f"Item not found for deletion: {pk}")
            return Response({"detail": "Item not found."}, status=status.HTTP_404_NOT_FOUND)

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = UserSerializer  # Adjust as needed
