from django.db.models import Count
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ParseError
from rest_framework.request import Request
from rest_framework.response import Response
from taggit.models import Tag
from ..models import Post
from .serializers import PostSerializer, TagSerializer


# ViewSets define the view behavior.
class PostViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Post.published.all()
    serializer_class = PostSerializer

    @action(detail=False)
    def latest(self, request: Request, *args, **kwargs):
        limit_text = request.query_params.get("limit", "5")
        if not limit_text.isdigit():
            raise ParseError("`limit` query param must be an integer.")

        latest_posts = Post.published.all().order_by("-publish")[: int(limit_text)]

        page = self.paginate_queryset(latest_posts)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(latest_posts, many=True)
        return Response(serializer.data)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    post_ids = Post.published.values("id")

    queryset = Tag.objects.filter(
        taggit_taggeditem_items__content_type__app_label="blog",
        taggit_taggeditem_items__content_type__model="post",
        taggit_taggeditem_items__object_id__in=post_ids,
    ).annotate(count=Count("*"))
    serializer_class = TagSerializer
