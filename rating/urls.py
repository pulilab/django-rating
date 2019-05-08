from rest_framework.routers import DefaultRouter

from .views import ObjectRatingViewSet, RatingElementViewSet

router = DefaultRouter()
router.register(r'objectratings', ObjectRatingViewSet)
router.register(r'ratingelements', RatingElementViewSet)

urlpatterns = router.urls
