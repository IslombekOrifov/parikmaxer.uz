from django.urls import path

from api.v1.accounts.views import (
    UserRegisterView, UserEditAPIView, UserRetrieveAPIView,
    ExperienceCreateAPIView, ExperienceDestroyAPIView,
    ExperienceListAPIView
)

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='auth_register'),
    path('detail/<int:pk>/', UserRetrieveAPIView.as_view(), name='user_detail'),
    path('update/', UserEditAPIView.as_view(), name='user_update'),

    path('experience/remove/<int:pk>/', ExperienceDestroyAPIView.as_view(), name='experience_delete'),
    path('experience/list/<slug:custom_id>/', ExperienceListAPIView.as_view(), name='experience_list'),
    path('experience/create/', ExperienceCreateAPIView.as_view(), name='experience_add'),

]
