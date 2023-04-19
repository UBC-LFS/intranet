from django.conf import settings
from django.db import models

from wagtail import blocks
from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel, FieldRowPanel
from wagtail.search import index
from wagtail.images.blocks import ImageChooserBlock
from wagtail.snippets.blocks import SnippetChooserBlock


class OperationsIndex(Page):
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

    subpage_types = ['OperationPage']


class OperationPage(Page):
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
        FieldPanel('body')
    ]

    parent_page_types = ['OperationsIndex']

