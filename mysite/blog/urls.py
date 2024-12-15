from django.urls import include, path
from rest_framework import routers

from .api import views as api_views

app_name = "blog"  # Application namespace

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r"posts", api_views.PostViewSet)
router.register(r"tags", api_views.TagViewSet)
router.register(r"comments", api_views.CommentViewSet)
router.register(r"projects", api_views.ProjectViewSet)

urlpatterns = [
    path("api/", include(router.urls)),
    path(
        "api/posts/<int:year>/<int:month>/<int:day>/<slug:slug>/",
        api_views.PostViewSet.as_view({"get": "retrieve"}),
        name="post-detail",
    ),
    path(
        "api/posts/<int:year>/<int:month>/<int:day>/<slug:slug>/similar/",
        api_views.PostViewSet.as_view({"get": "similar"}),
        name="post-similar",
    ),
]
