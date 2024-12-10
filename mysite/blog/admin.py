from django.contrib import admin
from django.db import models
from martor.widgets import AdminMartorWidget

from .models import Comment, Post, Project

# Register your models here.


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    class Media:
        css = {"all": ["css/custom-martor-admin.css"]}

    list_display = ["title", "slug", "author", "publish", "status"]
    list_filter = ["status", "created", "publish", "author"]
    search_fields = ["title", "body"]  # Search bar
    prepopulated_fields = {"slug": ("title",)}
    raw_id_fields = ["author"]  # User lookup widget
    date_hierarchy = "publish"  # Date breadcrumbs (below search bar)
    # ordering = ["status", "publish"]  # Overrides the default sort order of the model.
    show_facets = admin.ShowFacets.ALWAYS  # Object counts for each filter.
    formField_overrides = {
        models.TextField: {"widget": AdminMartorWidget},
    }


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "post", "created", "active"]
    list_filter = ["active", "created", "updated"]
    search_fields = ["name", "email", "body"]


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ["title", "link", "thumbnail"]
