from django.conf import settings  # Project's settings
from django.db import models
from django.urls import reverse
from django.utils import timezone
from taggit.managers import TaggableManager

# from django.db.models.functions import Now


class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class Post(TimeStampedModel):
    class Status(models.TextChoices):  # Enum type (choices)
        DRAFT = "DF", "Draft"
        PUBLISHED = "PB", "Published"

    # * Model fields
    title = models.CharField(max_length=250)  # VARCHAR column
    # Short label that contains only letters, numbers, underscores, or hyphens
    #   for building SEO-friendly URLs.
    slug = models.SlugField(max_length=250, unique_for_date="publish")  # VARCHAR column
    # Defines a many-to-one relationship (One author can write many posts).
    # `related_name` specifies the name of the reverse relationship, `user.blog_posts`.
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="blog_posts"
    )
    body = models.TextField()  # TEXT column
    publish = models.DateTimeField(default=timezone.now)  # DATETIME column
    # publish = models.DateTimeField(db_default=Now())  # Database-computed (introduced in Django 5)
    status = models.CharField(max_length=2, choices=Status, default=Status.DRAFT)
    summary = models.TextField(default="")

    # * Model managers
    # First manager defined becomes default manager.
    # Django will not create the `objects` manager if the model defines
    #   another manager. So, define it explicitly to keep it.
    objects = models.Manager()
    published = PublishedManager()  # Our custom manager.
    tags = TaggableManager()

    # * Model metadata
    class Meta:
        ordering = ["-publish"]  # Defines a default sort order.
        indexes = [
            models.Index(fields=["-publish"]),
        ]
        # default_manager_name = "published"  # Specifies a different default manager.

    def __str__(self):
        return self.title

    # Canonical URL - preferred/most representative/main URL for a resource.
    def get_absolute_url(self):
        # `reverse()` is a URL resolver that build the URL dynamically using
        #   the URL name defined in the `blog/urls.py`.
        return reverse(
            "blog:post_detail",
            args=[self.publish.year, self.publish.month, self.publish.day, self.slug],
        )


class Comment(TimeStampedModel):
    # One post can have many comments.
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    active = models.BooleanField(default=True)  # Controls the status of the comment.

    class Meta:
        ordering = ["created"]
        indexes = [
            # Improve ordering and searching performance.
            models.Index(fields=["created"]),
        ]

    def __str__(self):
        return f"Comment by {self.name} on {self.post}"


class Project(TimeStampedModel):
    title = models.CharField(max_length=250)
    description = models.TextField()
    link = models.URLField(max_length=200)
    # Subclass of `FileField`.
    #   `upload_to` arg accepts callable.
    #   Use `{{ object.thumbnail.url }}` to get the absolute path in a template.
    # ! Saving and loading images from a single large directory would slow down the system.
    thumbnail = models.ImageField(upload_to="images/%Y/%m/%d/")

    def __str__(self):
        return self.title
