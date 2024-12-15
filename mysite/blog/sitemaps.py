from django.contrib.sitemaps import Sitemap
from taggit.models import Tag

from .models import Post


class PostSitemap(Sitemap):
    changefreq = "weekly"  # Change frequency of post pages.
    priority = 0.9  # Relevance of post pages in the website. (max: 1)

    def items(self):
        return Post.published.all()  # Objects to include in this sitemap.

    def lastmod(self, obj: Post):
        return obj.updated


class TagSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        return Tag.objects.all()

    def location(self, obj: Tag):
        return f"/tags/{obj.slug}/page/1"
