from django.urls import path
from .views import UserRegistrationView
# #  UserLoginView,ItemViewSet
# from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    # path('login/', UserLoginView.as_view(), name='user-login'),
    # path('items/', ItemList.as_view(), name='item-list'),
    # path('items/<int:item_id>/', ItemDetail.as_view(), name='item-detail'),
    # path('token/', UserLoginView.as_view(), name='login'),  # Use this if not customizing
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]