from django.urls import path
from .views import UserRegistrationView,UserLoginView,ItemCreationView,ItemDetailView,ItemUpdateView,ItemDeleteView
# #  UserLoginView,ItemViewSet
# from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('items/', ItemCreationView.as_view(), name='item-create'),
    path('items/<int:pk>/', ItemDetailView.as_view(), name='item-detail'),
    path('items/<int:pk>/update/', ItemUpdateView.as_view(), name='item-update'),
    path('items/<int:pk>/delete/', ItemDeleteView.as_view(), name='item-delete'),
    # path('items/', ItemList.as_view(), name='item-list'),
    # path('items/<int:item_id>/', ItemDetail.as_view(), name='item-detail'),
    # path('token/', UserLoginView.as_view(), name='login'),  # Use this if not customizing
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]