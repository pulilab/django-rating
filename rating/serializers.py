from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .rating_values import RatingValues
from .models import ObjectRating, RatingElement


class RatingElementSerializer(serializers.ModelSerializer):

    class Meta:
        model = RatingElement
        fields = '__all__'

    @staticmethod
    def validate_element_type(value):
        if value in [item[0] for item in RatingValues.VALID_ELEMENT_TYPES]:
            return value
        raise ValidationError('Invalid element type.')

    @staticmethod
    def validate_score(value):
        if value and (value < RatingValues.MIN_SCORE or value > RatingValues.MAX_SCORE):
            raise ValidationError('Invalid score.')
        return value


class ObjectRatingSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = ObjectRating
        fields = '__all__'

    @staticmethod
    def validate_user_type(value):
        if value in [item[0] for item in RatingValues.VALID_USER_TYPES]:
            return value
        raise ValidationError('Invalid user type.')
