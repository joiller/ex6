from django.urls import path,re_path, include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('accounts', AccountViewSet)
router.register('product', ProductViewSet)
router.register('transactions', TransactionViewSet)

# router.register('register', AccountRegisterView)

# router.register('products')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', AccountRegisterView.as_view()),
    path('login/', AccountLoginView().as_view()),
    path('profile/<str:name>', AccountProfileView.as_view()),
    path('purchase/', PurchaseView.as_view()),

]
