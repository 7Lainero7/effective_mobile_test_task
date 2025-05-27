from rest_framework.routers import DefaultRouter

from .views import AdViewSet, ExchangeProposalViewSet, UserViewSet


router = DefaultRouter()
router.register(r'ads', AdViewSet, basename='ad')
router.register(r'proposals', ExchangeProposalViewSet)
router.register(r'users', UserViewSet)

urlpatterns = router.urls
