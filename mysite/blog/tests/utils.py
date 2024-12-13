from django.contrib.auth.models import User
from django.utils import timezone

from ..models import Comment, Post, Project


def populate_initial_data():
    user = User.objects.create_user("john", pk=1)

    posts = Post.objects.bulk_create(
        [
            Post(
                id=1,
                title="Post A",
                slug="post-a",
                publish=timezone.datetime(
                    2024, 3, 2, tzinfo=timezone.get_current_timezone()
                ),
                status=Post.Status.PUBLISHED,
                author=user,
            ),
            Post(
                id=2,
                title="Post B",
                slug="post-b",
                publish=timezone.datetime(
                    2024, 5, 6, tzinfo=timezone.get_current_timezone()
                ),
                status=Post.Status.PUBLISHED,
                author=user,
            ),
            Post(
                id=3,
                title="Post C",
                slug="post-c",
                publish=timezone.datetime(
                    2024, 2, 4, tzinfo=timezone.get_current_timezone()
                ),
                status=Post.Status.PUBLISHED,
                author=user,
            ),
            Post(
                id=4,
                title="Post AAA",
                slug="post-aaa",
                publish=timezone.datetime(
                    2024, 2, 2, tzinfo=timezone.get_current_timezone()
                ),
                status=Post.Status.PUBLISHED,
                author=user,
            ),
        ]
    )

    posts[0].tags.add("testing", "a")
    posts[1].tags.add("testing")
    posts[2].tags.add("c")
    posts[3].tags.add("testing", "a")

    Comment.objects.create(id=1, post=posts[0], name="wick", body="Good comment")
    Comment.objects.create(id=2, post=posts[0], name="wick", body="Bad comment")
    Comment.objects.create(id=3, post=posts[1], name="wick", body="No comment")

    Project.objects.create(id=1, title="Blog")
