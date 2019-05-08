from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .models import ObjectRating, RatingElement
from .serializers import ObjectRatingSerializer, RatingElementSerializer


class RatingElementViewSet(ModelViewSet):
    queryset = RatingElement.objects.all()
    serializer_class = RatingElementSerializer
    permission_classes = (IsAuthenticated, )


class ObjectRatingViewSet(ModelViewSet):
    queryset = ObjectRating.objects.all()
    serializer_class = ObjectRatingSerializer
    permission_classes = (IsAuthenticated, )
