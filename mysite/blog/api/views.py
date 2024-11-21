from functools import partial
from typing import cast
from django.shortcuts import get_object_or_404
from django.db.models import Count
from django.contrib.postgres.search import TrigramSimilarity
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.exceptions import ParseError
from rest_framework.request import Request
from rest_framework.response import Response
from taggit.models import Tag
from .serializers import PostSerializer, TagSerializer, CommentSerializer
from .views_utils import get_pagable_response
from .pagination import DynamicPageNumberPagination
from ..models import Post, Comment


# ViewSets define the view behavior.
class PostViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Post.published.all()
    pagination_class = staticmethod(partial(DynamicPageNumberPagination, page_size=5))

    def get_object(self):
        url_kwargs: dict[str, str] = self.kwargs

        pk = url_kwargs.get("pk")
        if pk is not None:
            if not pk.isdigit():
                raise ParseError(
                    f"`pk` URL param must be an integer, such as /api/posts/6/"
                )
            return get_object_or_404(Post.published.all(), pk=pk)

        lookup_kwargs = {
            "publish__year": url_kwargs.get("year"),
            "publish__month": url_kwargs.get("month"),
            "publish__day": url_kwargs.get("day"),
            "slug": url_kwargs.get("slug"),
        }
        return get_object_or_404(Post.published.all(), **lookup_kwargs)

    def get_serializer(self, *args, **kwargs):
        # Discard duplicate keyword argument.
        kwargs.pop("context", None)

        PartialSerializer = partial(
            PostSerializer, *args, **kwargs, context={"request": self.request}
        )

        if self.action in ["list", "latest", "search", "similar"]:
            return PartialSerializer(exclude=["body"])
        return PartialSerializer()

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

    @action(detail=True)
    def similar(self, request: Request, *args, **kwargs):
        """
        Supported query string:\n
        - `limit`: Accepts an integer value. (e.g. `?limit=10`)
        """
        limit_text = request.query_params.get("limit", "5")
        if not limit_text.isdigit():
            raise ParseError("`limit` query param must be an integer.")

        post: Post = self.get_object()
        post_tags_ids = post.tags.values_list("id", flat=True)
        similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(
            id=post.id
        )
        similar_posts = similar_posts.annotate(same_tags=Count("tags")).order_by(
            "-same_tags", "-publish"
        )[: int(limit_text)]

        return get_pagable_response(self, similar_posts, self.get_serializer)

    def retrieve(self, request, *args, **kwargs):
        curr_post = self.get_object()
        prev_post = Post.published.filter(id__lt=curr_post.id).order_by("-id").first()
        next_post = Post.published.filter(id__gt=curr_post.id).order_by("id").first()

        fields = ["url", "url_alt", "id", "title", "slug", "publish"]

        curr_data = self.get_serializer(curr_post).data
        prev_data = (
            self.get_serializer(prev_post, fields=fields).data
            if prev_post is not None
            else None
        )
        next_data = (
            self.get_serializer(next_post, fields=fields).data
            if next_post is not None
            else None
        )

        return Response({**curr_data, "previous": prev_data, "next": next_data})


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    post_ids = Post.published.values("id")
    queryset = (
        Tag.objects.filter(
            taggit_taggeditem_items__content_type__app_label="blog",
            taggit_taggeditem_items__content_type__model="post",
            taggit_taggeditem_items__object_id__in=post_ids,
        )
        .annotate(count=Count("*"))
        .order_by("-count")
    )
    serializer_class = TagSerializer
    lookup_field = "slug"
    pagination_class = staticmethod(partial(DynamicPageNumberPagination, page_size=20))

    @action(detail=True)
    def posts(self, request: Request, *args, **kwargs):
        tag = self.get_object()
        tag_posts = Post.published.filter(tags__in=[tag])
        return get_pagable_response(
            self,
            tag_posts,
            staticmethod(partial(PostSerializer, exclude=["body"])),
            PostViewSet.pagination_class,
        )


class CommentViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    """
    Supported query string:\n
    - `post_id`: Accepts an integer value. (e.g. `?post_id=6`)
    """

    queryset = Comment.objects.filter(active=True)
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_id = cast(Request, self.request).query_params.get("post_id")
        if post_id is None:
            return self.queryset

        if not post_id.isdigit():
            raise ParseError("`post_id` query param must be an integer.")

        return self.queryset.filter(post=post_id)
