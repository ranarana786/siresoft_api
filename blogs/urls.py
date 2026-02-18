from rest_framework.routers import DefaultRouter
from .views import BlogViewSet, CategoryViewSet

router = DefaultRouter()
router.register('blogs', BlogViewSet, basename='blogs')
router.register('categories', CategoryViewSet, basename='categories')

urlpatterns = router.urls
