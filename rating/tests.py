from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient

from .models import RatingElement, ObjectRating
from .rating_values import RatingValues


class TestObjectRatingAPI(APITestCase):
    PASS = 'secretpass'

    def setUp(self):
        super().setUp()

        self.user_1 = User.objects.create_user(
            'user_1@test.com', email='user_1@test.com', password=self.PASS)
        self.user_2 = User.objects.create_user(
            'user_2@test.com', email='user_2@test.com', password=self.PASS)

        self.user_client = APIClient()
        self.user_client.login(username='user_1@test.com', password=self.PASS)

        self.perm = Permission.objects.first()
        self.perm_c_t = ContentType.objects.get(model='permission')

        self.element_type = RatingValues.VALID_ELEMENT_TYPES[0][0]
        self.user_type = RatingValues.VALID_USER_TYPES[0][0]

    def test_create_rating_element_success(self):
        data = {
            'element_type': self.element_type,
            'score': 5,
        }
        url = reverse('ratingelement-list')
        response = self.user_client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        resp_json = response.json()
        self.assertEqual(resp_json['element_type'], self.element_type)
        self.assertEqual(resp_json['score'], 5)
        self.assertEqual(resp_json['comment'], None)

    def test_create_rating_element_with_invalid_type_fail(self):
        data = {
            'element_type': 'invalid element type',
            'score': 5,
        }
        url = reverse('ratingelement-list')
        response = self.user_client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'element_type': ['Invalid element type.']})

    def test_create_rating_element_with_score_too_low_fail(self):
        data = {
            'element_type': self.element_type,
            'score': -1,
        }
        url = reverse('ratingelement-list')
        response = self.user_client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'score': ['Invalid score.']})

    def test_create_rating_element_with_score_too_high_fail(self):
        data = {
            'element_type': self.element_type,
            'score': 11,
        }
        url = reverse('ratingelement-list')
        response = self.user_client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'score': ['Invalid score.']})

    def test_get_rating_element(self):
        element = RatingElement.objects.create(
            element_type=self.element_type, score=10, comment='super'
        )
        url = reverse('ratingelement-detail', args=(element.id,))
        response = self.user_client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        resp_json = response.json()
        self.assertEqual(resp_json['element_type'], self.element_type)
        self.assertEqual(resp_json['score'], 10)
        self.assertEqual(resp_json['comment'], 'super')

    def test_list_rating_elements(self):
        RatingElement.objects.create(element_type=self.element_type, score=10, comment='super')
        RatingElement.objects.create(element_type=self.element_type, score=9, comment='good')
        url = reverse('ratingelement-list')
        response = self.user_client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 2)

    def test_update_rating_element(self):
        element = RatingElement.objects.create(element_type=self.element_type, score=5,)
        data = {'score': 4}
        url = reverse('ratingelement-detail', args=(element.id,))
        response = self.user_client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        resp_json = response.json()
        self.assertEqual(resp_json['element_type'], self.element_type)
        self.assertEqual(resp_json['score'], 4)

    def test_delete_rating_element(self):
        element = RatingElement.objects.create(element_type=self.element_type, score=5,)
        url = reverse('ratingelement-detail', args=(element.id,))
        response = self.user_client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_create_object_rating_with_invalid_user_type_fail(self):
        element = RatingElement.objects.create(element_type=self.element_type, score=10, comment='super')
        data = {
            'user_type': 'invalid type',
            'object_id': self.perm.id,
            'content_type': self.perm_c_t.id,
            'elements': [element.id]
        }
        url = reverse('objectrating-list')
        response = self.user_client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'user_type': ['Invalid user type.']})

    def test_create_object_rating_success(self):
        element = RatingElement.objects.create(element_type=self.element_type, score=10, comment='super')
        data = {
            'user_type': self.user_type,
            'object_id': self.perm.id,
            'content_type': self.perm_c_t.id,
            'elements': [element.id]
        }
        url = reverse('objectrating-list')
        response = self.user_client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        resp_json = response.json()
        self.assertEqual(resp_json['user_type'], self.user_type)
        self.assertEqual(resp_json['object_id'], self.perm.id)
        self.assertEqual(resp_json['content_type'], self.perm_c_t.id)
        self.assertEqual(resp_json['elements'], [element.id])

    def test_list_objects_ratings(self):
        element_1 = RatingElement.objects.create(element_type=self.element_type, score=10, comment='super')
        object_rating_1 = ObjectRating.objects.create(
            user=self.user_1, user_type=self.user_type,
            object_id=self.perm.id, content_type=self.perm_c_t,
        )
        object_rating_1.elements.add(element_1)

        element_2 = RatingElement.objects.create(element_type=self.element_type, score=9, comment='good')
        object_rating_2 = ObjectRating.objects.create(
            user=self.user_2, user_type=self.user_type,
            object_id=self.perm.id, content_type=self.perm_c_t
        )
        object_rating_2.elements.add(element_2)

        url = reverse('objectrating-list')
        response = self.user_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 2)

    def test_get_object_rating(self):
        element = RatingElement.objects.create(element_type=self.element_type, score=10, comment='super')
        object_rating = ObjectRating.objects.create(
            user=self.user_1, user_type=self.user_type,
            object_id=self.perm.id, content_type=self.perm_c_t,
        )
        object_rating.elements.add(element)

        url = reverse('objectrating-detail', args=(object_rating.id,))
        response = self.user_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        resp_json = response.json()
        self.assertEqual(resp_json['user_type'], self.user_type)
        self.assertEqual(resp_json['object_id'], self.perm.id)
        self.assertEqual(resp_json['content_type'], self.perm_c_t.id)
        self.assertEqual(resp_json['elements'], [element.id])

    def test_update_object_rating(self):
        element_1 = RatingElement.objects.create(element_type=self.element_type, score=10)
        element_2 = RatingElement.objects.create(element_type=self.element_type, comment='super')
        object_rating = ObjectRating.objects.create(
            user=self.user_1, user_type=self.user_type,
            object_id=self.perm.id, content_type=self.perm_c_t,
        )
        object_rating.elements.add(element_1)

        self.assertEqual(object_rating.elements.count(), 1)

        data = {'elements': [element_1.id, element_2.id]}
        url = reverse('objectrating-detail', args=(object_rating.id,))
        response = self.user_client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['elements'], [element_1.id, element_2.id])

    def test_delete_object_rating(self):
        element = RatingElement.objects.create(element_type=self.element_type, score=10, comment='super')
        object_rating = ObjectRating.objects.create(
            user=self.user_1, user_type=self.user_type,
            object_id=self.perm.id, content_type=self.perm_c_t,
        )
        object_rating.elements.add(element)

        url = reverse('objectrating-detail', args=(object_rating.id,))
        response = self.user_client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
