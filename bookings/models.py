from django.db import models
from modelcluster.fields import ParentalKey
from taggit.models import Tag, TaggedItemBase
from core.models import IndexModel, PageModel
from modelcluster.contrib.taggit import ClusterTaggableManager


class BookingTag(TaggedItemBase):
    content_object = ParentalKey('BookingPage', related_name='tagged_items', on_delete=models.CASCADE)

class BookingPage(PageModel):
    tags = ClusterTaggableManager(through=BookingTag, blank=True)
    parent_page_types = ['BookingsIndex']

class BookingsIndex(IndexModel):
    subpage_types = ['BookingPage']
