from django.urls import path
from .views import Index, ConfirmUser, ProfileView

urlpatterns = [
    path('', Index.as_view(), name='index'),  # http://127.0.0.1:8025
    path('confirm/', ConfirmUser.as_view(), name='confirm_user'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('accounts/', Index.as_view(), name='index'),  #  временно  http://127.0.0.1:8025/accounts
 #   path('messages/'?),
]