from rest_framework import serializers
from taggit.models import Tag
from taggit.serializers import TagListSerializerField, TaggitSerializer
from ..models import Post, Comment, Project
from . import serializers_utils


# Serializers define the API representation.
class PostSerializer(TaggitSerializer, serializers.HyperlinkedModelSerializer):
    url = serializers_utils.PostHyperlink(view_name="blog:post-detail")
    url_alt = serializers.HyperlinkedIdentityField(view_name="blog:post-detail")
    id = serializers.IntegerField(read_only=True)
    author = serializers.SlugRelatedField(
        many=False, read_only=True, slug_field="username"
    )
    tags = TagListSerializerField()

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
    url = serializers.HyperlinkedIdentityField(
        view_name="blog:tag-detail", lookup_field="slug"
    )
    id = serializers.IntegerField(read_only=True)
    count = serializers.IntegerField()

    class Meta:
        model = Tag
        fields = "__all__"


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="blog:comment-detail")
    id = serializers.IntegerField(read_only=True)
    post = serializers.HyperlinkedRelatedField(
        read_only=True, view_name="blog:post-detail"
    )
    post_id = serializers.PrimaryKeyRelatedField(
        queryset=Post.published.all().values_list("id", flat=True)
    )

    class Meta:
        model = Comment
        fields = "__all__"


class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="blog:project-detail")
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Project
        fields = "__all__"
