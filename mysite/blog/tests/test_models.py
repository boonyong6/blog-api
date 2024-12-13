from django.test import TestCase

from ..models import Comment, Post, Project
from .utils import populate_initial_data


class PostTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        populate_initial_data()

    def test_str_returns_title(self):
        post: Post = Post.published.get(pk=2)
        self.assertEqual(str(post), "Post B")

    def test_get_absolute_url(self):
        post: Post = Post.published.get(pk=2)
        url = post.get_absolute_url()
        self.assertEqual(url, "/2024/5/6/post-b/")


class CommentTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        populate_initial_data()

    def test_str_returns_formatted_string(self):
        comment: Comment = Comment.objects.get(pk=1)
        self.assertEqual(str(comment), "Comment by wick on Post A")


class ProjectTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        populate_initial_data()

    def test_str_returns_title(self):
        project: Project = Project.objects.get(pk=1)
        self.assertEqual(str(project), "Blog")
