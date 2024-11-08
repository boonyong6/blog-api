from rest_framework import viewsets
from ..models import Post
from .serializers import PostSerializer


# ViewSets define the view behavior.
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.published
    serializer_class = PostSerializer
