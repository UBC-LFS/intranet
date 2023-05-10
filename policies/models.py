from django.conf import settings
from django.db import models

from wagtail import blocks
from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel
from wagtail.search import index
from wagtail.images.blocks import ImageChooserBlock
from wagtail.snippets.blocks import SnippetChooserBlock

from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import Tag, TaggedItemBase
from wagtail.contrib.routable_page.models import RoutablePageMixin, route

from django.shortcuts import redirect, render


class PolicyTag(TaggedItemBase):
    content_object = ParentalKey(
        'PolicyPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )


class PolicyPage(Page):
    publish_date = models.DateField('Publish date', blank=True, null=True)
    body = StreamField([
        ('visual', blocks.RichTextBlock(features=settings.RICH_TEXT_FEATURES)),
        ('html', blocks.RawHTMLBlock()),
        ('image', ImageChooserBlock())
    ], use_json_field=True, blank=True)
    tags = ClusterTaggableManager(through=PolicyTag, blank=True)

    search_fields = Page.search_fields + [
        index.SearchField('body')
    ]

    content_panels = Page.content_panels + [
        FieldPanel('publish_date'),
        FieldPanel('body'),
        FieldPanel('tags')
    ]

    parent_page_types = ['PoliciesIndex']
    subpage_types = []

    @property
    def get_tags(self):
        tags = self.tags.all()
        base_url = self.get_parent().url
        for tag in tags:
            tag.url = f"{base_url}tags/{tag.slug}/"
        return tags


class PoliciesIndex(RoutablePageMixin, Page):
    publish_date = models.DateField('Publish date', blank=True, null=True)
    body = StreamField([
        ('visual', blocks.RichTextBlock(features=settings.RICH_TEXT_FEATURES)),
        ('html', blocks.RawHTMLBlock()),
        ('image', ImageChooserBlock())
    ], use_json_field=True, blank=True)

    search_fields = Page.search_fields + [
        index.SearchField('body')
    ]

    content_panels = Page.content_panels + [
        FieldPanel('publish_date'),
        FieldPanel('body'),
    ]

    subpage_types = ['PolicyPage']

    def children(self):
        return self.get_children().specific().live()

    def get_context(self, request):
        context = super(PoliciesIndex, self).get_context(request)
        context["posts"] = (
            PolicyPage.objects.descendant_of(self).live().order_by("-publish_date")
        )
        return context

    def get_posts(self, tag=None):
        posts = PolicyPage.objects.live().descendant_of(self)
        if tag:
            posts = posts.filter(tags=tag)
        return posts

    def serve_preview(self, request, mode_name):
        return self.serve(request)

    def get_child_tags(self):
        tags = []
        for post in self.get_posts():
            tags += post.get_tags
        tags = sorted(set(tags))
        return tags

    @route(r"^tags/$", name="tag_archive")
    @route(r"^tags/([\w-]+)/$", name="tag_archive")
    def tag_archive(self, request, tag=None):
        try:
            tag = Tag.objects.get(slug=tag)
        except Tag.DoesNotExist:
            if tag:
                msg = 'There are no posts tagged with "{}"'.format(tag)
                messages.add_message(request, messages.INFO, msg)
            return redirect(self.url)

        posts = self.get_posts(tag=tag)
        context = { "model": "policies", "url": "/policies/", "tag": tag, "posts": posts }
        return render(request, "policies/policies_index.html", context)