from django.conf import settings


class RatingValues:
    DEFAULT_USER_TYPES = (
        ('U', 'USER_TYPE'),
    )
    DEFAULT_ELEMENT_TYPES = (
        ('E', 'ELEMENT_TYPE'),
    )

    VALID_USER_TYPES = getattr(settings, 'RATING_VALID_USER_TYPES', DEFAULT_USER_TYPES)
    VALID_ELEMENT_TYPES = getattr(settings, 'RATING_VALID_ELEMENT_TYPES', DEFAULT_ELEMENT_TYPES)
    MIN_SCORE = getattr(settings, 'RATING_MIN_SCORE', 0)
    MAX_SCORE = getattr(settings, 'RATING_MAX_SCORE', 10)
