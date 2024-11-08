from rest_framework import serializers
from ..models import Post


# Serializers define the API representation.
class PostSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.SlugRelatedField(
        many=False, read_only=True, slug_field="username"
    )

    tags = serializers.SlugRelatedField(many=True, read_only=True, slug_field="name")

    url = serializers.HyperlinkedIdentityField(view_name="blog:post-detail")

    class Meta:
        model = Post
        fields = "__all__"
