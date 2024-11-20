from rest_framework import serializers
from taggit.models import Tag
from taggit.serializers import TagListSerializerField, TaggitSerializer
from ..models import Post
from . import serializers_utils


# Serializers define the API representation.
class PostSerializer(TaggitSerializer, serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField()
    author = serializers.SlugRelatedField(
        many=False, read_only=True, slug_field="username"
    )
    tags = TagListSerializerField()
    url = serializers_utils.PostHyperlink(view_name="blog:post-detail")
    url_alt = serializers.HyperlinkedIdentityField(view_name="blog:post-detail")

    class Meta:
        model = Post
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        # Don't pass the `exclude` arg up to the superclass.
        excluded_fields = kwargs.pop("exclude", [])

        super().__init__(*args, **kwargs)

        # Exclude fields specified in the `exclude` argument.
        for field in excluded_fields:
            self.fields.pop(field, None)


class TagSerializer(serializers.HyperlinkedModelSerializer):
    count = serializers.IntegerField()
    url = serializers.HyperlinkedIdentityField(
        view_name="blog:tag-detail", lookup_field="slug"
    )

    class Meta:
        model = Tag
        fields = "__all__"
