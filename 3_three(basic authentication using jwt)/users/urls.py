"""
Docstring for users.urls
"""
# core imports
from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


# local imports
# from .views import(
#     profile
# )

urlpatterns = [
    

    # token verification
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),    
]