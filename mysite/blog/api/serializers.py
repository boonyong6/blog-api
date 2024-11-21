from rest_framework import serializers
from taggit.models import Tag
from taggit.serializers import TagListSerializerField, TaggitSerializer
from ..models import Post, Comment
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
        # Don't pass the `fields` and `exclude` arg up to the superclass.
        fields = kwargs.pop("fields", None)
        excluded_fields = kwargs.pop("exclude", None)

        if fields is not None and excluded_fields is not None:
            raise AssertionError(
                f"Cannot set both `fields` and `exclude` arguments when instantiating {PostSerializer.__name__}."
            )

        super().__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

        # Exclude fields specified in the `exclude` argument.
        if excluded_fields is not None:
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


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="blog:comment-detail")
    post = serializers.HyperlinkedRelatedField(
        view_name="blog:post-detail", queryset=Post.published.all()
    )

    class Meta:
        model = Comment
        fields = "__all__"
