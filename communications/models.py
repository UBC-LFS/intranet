from django.db import models
from modelcluster.fields import ParentalKey
from taggit.models import Tag, TaggedItemBase
from core.models import IndexModel, PageModel
from modelcluster.contrib.taggit import ClusterTaggableManager


class CommunicationTag(TaggedItemBase):
    content_object = ParentalKey('CommunicationPage', related_name='tagged_items', on_delete=models.CASCADE)

class CommunicationPage(PageModel):
    tags = ClusterTaggableManager(through=CommunicationTag, blank=True)
    parent_page_types = ['CommunicationsIndex']

class CommunicationsIndex(IndexModel):
    subpage_types = ['CommunicationPage']