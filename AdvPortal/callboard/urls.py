from django.urls import path
from callboard.views.advert import Index, ConfirmUser, ProfileView, AdvertList, AdvertCreate, \
    AdvertDetail, AdvertUpdate, AdvertDelete

urlpatterns = [
    path('', Index.as_view(), name='index'),  # http://127.0.0.1:8025
    path('callboard/', AdvertList.as_view(), name='advert_list'),  # {% url "advert_list" %}
    path('callboard/<int:pk>', AdvertDetail.as_view(), name='advert_detail'),
    path('callboard/create', AdvertCreate.as_view(), name='advert_create'),
    path('callboard/update/<int:pk>', AdvertUpdate.as_view(), name='advert_update'),
    path('callboard/delete/<int:pk>', AdvertDelete.as_view(), name='advert_delete'),

    path('confirm/', ConfirmUser.as_view(), name='confirm_user'),
    path('profile/', ProfileView.as_view(), name='profile'),

    path('accounts/', Index.as_view(), name='index'),  #  временно  http://127.0.0.1:8025/accounts
 #   path('messages/'?),
]
