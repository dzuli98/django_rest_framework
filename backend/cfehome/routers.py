from rest_framework.routers import DefaultRouter

from products.viewsets import ProductViewSet

router = DefaultRouter()
router.register('product-abc', ProductViewSet, basename='products')
print(router.urls)
urlpatterns = router.urls

# bad point is that it is hard to know witch serializers are being used