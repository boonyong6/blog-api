from django.test import TestCase

from ...api.serializers import PostSerializer
from ...models import Post


class PostSerializerTestCase(TestCase):
    def test_init_when_both_fields_and_exclude_are_given_raises_error(self):
        self.assertRaisesMessage(
            AssertionError,
            "Cannot set both `fields` and `exclude` arguments",
            PostSerializer,
            Post(),
            fields=["id"],
            exclude=["id"],
        )
