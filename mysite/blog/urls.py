from django.urls import path, include
from rest_framework import routers
from . import views
from .api import views as api_views
from .feeds import LatestPostsFeed

app_name = "blog"  # Application namespace

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r"posts", api_views.PostViewSet)
router.register(r"tags", api_views.TagViewSet)
router.register(r"comments", api_views.CommentViewSet)

urlpatterns = [
    # * Post views
    path("", views.post_list, name="post_list"),
    # path("", views.PostListView.as_view(), name="post_list"),
    path("tag/<slug:tag_slug>/", views.post_list, name="post_list_by_tag"),
    # Use `<>` to capture values from the URL.
    path(
        "<int:year>/<int:month>/<int:day>/<slug:post>/",
        views.post_detail,
        name="post_detail",
    ),
    path("<int:post_id>/share/", views.post_share, name="post_share"),
    path("<int:post_id>/comment/", views.post_comment, name="post_comment"),
    path("feed/", LatestPostsFeed(), name="post_feed"),
    path("search/", views.post_search, name="post_search"),
    path("api/", include(router.urls)),
    path(
        "api/posts/<int:year>/<int:month>/<int:day>/<slug:slug>/",
        api_views.PostViewSet.as_view({"get": "retrieve"}),
        name="post-detail",
    ),
    path(
        "api/posts/<int:year>/<int:month>/<int:day>/<slug:slug>/similar",
        api_views.PostViewSet.as_view({"get": "similar"}),
        name="post-similar",
    ),
]
