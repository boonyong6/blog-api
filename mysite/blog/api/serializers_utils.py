from rest_framework import serializers
from rest_framework.reverse import reverse
from ..models import Post


class PostHyperlink(serializers.HyperlinkedIdentityField):
    def get_url(self, obj: Post, view_name, request, format):
        url_kwargs = {
            "year": obj.publish.year,
            "month": obj.publish.month,
            "day": obj.publish.day,
            "slug": obj.slug,
        }
        return reverse(view_name, kwargs=url_kwargs, request=request, format=format)
