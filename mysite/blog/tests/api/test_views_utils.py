from rest_framework.test import APITestCase

from ...api.serializers import PostSerializer
from ...api.views import PostViewSet
from ...api.views_utils import get_pagable_response
from ..utils import populate_initial_data


class UtilsTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        populate_initial_data()

    def test_get_pagable_response_when_no_pagination_returns_unpaged_response(self):
        viewset = PostViewSet(pagination_class=None, request=None)

        response = get_pagable_response(
            viewset,
            viewset.queryset,
            PostSerializer,
        )

        self.assertIsInstance(response.data, list)
