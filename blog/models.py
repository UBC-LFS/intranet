from django.conf import settings
from django.db import models
from wagtail import blocks
from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel
from wagtail.search import index
from wagtail.images.blocks import ImageChooserBlock
from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase
from wagtail.contrib.routable_page.models import RoutablePageMixin

from .blocks import AccordionBlock, ColumnsBlock, CustomTableBlock
from core.functions import *


from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, FieldRowPanel, InlinePanel, MultiFieldPanel
from wagtail.fields import RichTextField
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField


class FormField(AbstractFormField):
    page = ParentalKey('FormPage', on_delete=models.CASCADE, related_name='form_fields')


class FormPage(AbstractEmailForm):
    intro = RichTextField(blank=True)
    thank_you_text = RichTextField(blank=True)

    content_panels = AbstractEmailForm.content_panels + [
        FieldPanel('intro'),
        InlinePanel('form_fields', label="Form fields"),
        FieldPanel('thank_you_text'),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname="col6"),
                FieldPanel('to_address', classname="col6"),
            ]),
            FieldPanel('subject'),
        ], "Email"),
    ]


class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey('BlogPage', related_name='tagged_items', on_delete=models.CASCADE)


class BlogPostTag(TaggedItemBase):
    content_object = ParentalKey('BlogPost', related_name='tagged_items', on_delete=models.CASCADE)


class BlogPost(Page):
    publish_date = models.DateField('Publish date', blank=True, null=True)
    
    body = StreamField([
        ('visual', blocks.RichTextBlock(features=settings.RICH_TEXT_FEATURES)),
        ('html', blocks.RawHTMLBlock()),
        ('image', ImageChooserBlock()),
        ('accordion', AccordionBlock()),
        ('columns', ColumnsBlock()),
        ('table', CustomTableBlock())
    ], use_json_field=True, blank=True)

    tags = ClusterTaggableManager(through=BlogPostTag, blank=True)

    search_fields = Page.search_fields + [
        index.SearchField('body')
    ]

    content_panels = Page.content_panels + [
        FieldPanel('publish_date'),
        FieldPanel('body'),
        FieldPanel('tags')
    ]
    
    parent_page_types = ['blog.BlogPage']
    subpage_types = []

    def get_context(self, request):
        context = super(BlogPost, self).get_context(request)
        context['model_name'] = self._meta.model_name
        context['sidebar_menu'] = make_sidebar_menu(request, get_user_groups(request), self.get_parent().get_parent())
        return context

    @property
    def get_tags(self):
        tags = self.tags.all()
        for tag in tags:
            tag.url = f"/search/?query={tag.slug}&method=tag&page=1"
        return tags


class BlogPage(Page):
    publish_date = models.DateField('Publish date', blank=True, null=True)
    body = StreamField([
        ('visual', blocks.RichTextBlock(features=settings.RICH_TEXT_FEATURES)),
        ('html', blocks.RawHTMLBlock()),
        ('image', ImageChooserBlock()),
        ('accordion', AccordionBlock()),
        ('columns', ColumnsBlock()),
        ('table', CustomTableBlock())
    ], use_json_field=True, blank=True)

    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)

    search_fields = Page.search_fields + [
        index.SearchField('body')
    ]

    content_panels = Page.content_panels + [
        FieldPanel('publish_date'),
        FieldPanel('body'),
        FieldPanel('tags')
    ]

    parent_page_types = ['blog.BlogIndex']
    subpage_types = ['blog.BlogPost']

    def get_context(self, request):
        context = super(BlogPage, self).get_context(request)
        context['model_name'] = self._meta.model_name
        context['sidebar_menu'] = make_sidebar_menu(request, get_user_groups(request), self.get_parent())
        return context

    @property
    def get_tags(self):
        tags = self.tags.all()
        for tag in tags:
            tag.url = f"/search/?query={tag.slug}&method=tag&page=1"
        return tags


class BlogIndex(RoutablePageMixin, Page):
    publish_date = models.DateField('Publish date', blank=True, null=True)
    body = StreamField([
        ('visual', blocks.RichTextBlock(features=settings.RICH_TEXT_FEATURES)),
        ('html', blocks.RawHTMLBlock()),
        ('image', ImageChooserBlock()),
        ('accordion', AccordionBlock()),
        ('columns', ColumnsBlock()),
        ('table', CustomTableBlock())
    ], use_json_field=True, blank=True)

    search_fields = Page.search_fields + [
        index.SearchField('body')
    ]

    content_panels = Page.content_panels + [
        FieldPanel('publish_date'),
        FieldPanel('body')
    ]

    subpage_types = ['blog.BlogPage']

    def get_context(self, request):
        context = super(BlogIndex, self).get_context(request)
        context['model_name'] = self._meta.model_name
        context['sidebar_menu'] = make_sidebar_menu(request, get_user_groups(request), self)
        return context