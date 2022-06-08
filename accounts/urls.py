from django.urls import path, include
from accounts import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('account', views.AccountViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # path('register/', views.Register.as_view(), name='register'),
    # path('login/', views.Login.as_view(), name='login'),
    path('create/', views.UserCreate.as_view()),
    path('change_password/',views.ChangePassword.as_view(), name='change-password'),
]
