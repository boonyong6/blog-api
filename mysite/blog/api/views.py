from django.db.models import Count
from django.contrib.postgres.search import TrigramSimilarity
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import ParseError
from rest_framework.request import Request
from rest_framework.response import Response
from taggit.models import Tag
from .serializers import PostSerializer, TagSerializer
from .viewutil import get_pagable_response
from ..models import Post


# ViewSets define the view behavior.
class PostViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Post.published.all()
    serializer_class = PostSerializer

    @action(detail=False)
    def latest(self, request: Request, *args, **kwargs):
        """
        Supported query string:\n
        - `limit`: Accepts an integer value. (e.g. `?limit=10`)
        """
        limit_text = request.query_params.get("limit", "5")
        if not limit_text.isdigit():
            raise ParseError("`limit` query param must be an integer.")

        latest_posts = Post.published.all().order_by("-publish")[: int(limit_text)]
        return get_pagable_response(self, latest_posts, self.get_serializer)

    @action(detail=False)
    def search(self, request: Request, *args, **kwargs):
        """
        Supported query string:\n
        - `query`: Accepts a text value. (e.g. `?query=django`)
        """
        query = request.query_params.get("query")
        similar_posts = (
            self.queryset.annotate(similarity=TrigramSimilarity("title", query))
            .filter(similarity__gt=0.1)
            .order_by("-similarity")
        )
        return get_pagable_response(self, similar_posts, self.get_serializer)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    post_ids = Post.published.values("id")

    queryset = Tag.objects.filter(
        taggit_taggeditem_items__content_type__app_label="blog",
        taggit_taggeditem_items__content_type__model="post",
        taggit_taggeditem_items__object_id__in=post_ids,
    ).annotate(count=Count("*"))
    serializer_class = TagSerializer

    @action(detail=True)
    def posts(self, request: Request, *args, **kwargs):
        tag = self.get_object()
        tag_posts = Post.published.filter(tags__in=[tag])
        return get_pagable_response(self, tag_posts, PostSerializer)
