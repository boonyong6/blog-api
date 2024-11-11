from rest_framework import serializers
from taggit.models import Tag
from taggit.serializers import TagListSerializerField, TaggitSerializer
from ..models import Post


# Serializers define the API representation.
class PostSerializer(TaggitSerializer, serializers.HyperlinkedModelSerializer):
    author = serializers.SlugRelatedField(
        many=False, read_only=True, slug_field="username"
    )
    tags = TagListSerializerField()
    url = serializers.HyperlinkedIdentityField(view_name="blog:post-detail")

    class Meta:
        model = Post
        fields = "__all__"


class TagSerializer(serializers.HyperlinkedModelSerializer):
    count = serializers.IntegerField()
    url = serializers.HyperlinkedIdentityField(view_name="blog:tag-detail")

    class Meta:
        model = Tag
        fields = "__all__"
