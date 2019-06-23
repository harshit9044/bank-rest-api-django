from django.urls import path
from django.conf.urls import include
from .views import BankDetailAPIView,AllBranchesAPIView
from rest_framework.routers import DefaultRouter

from rest_framework_simplejwt import views as jwt_views




router    = DefaultRouter()
router.register('bank-detail',BankDetailAPIView,base_name='bank-detail')
router.register('all-banks',AllBranchesAPIView,base_name='all-banks')
# router.register('token/',jwt_views.TokenObtainPairView, base_name='token_obtain_pair')
# router.register('token/refresh/', jwt_views.TokenRefreshView, base_name='token_refresh')


urlpatterns = [
	path('',include(router.urls)),
	path('token/',jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
	path('token-refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh')
	# path('bank-detail/',BankDetailAPIView.as_view()),
	# path('all-banks/',AllBranchesAPIView.as_view()),
]