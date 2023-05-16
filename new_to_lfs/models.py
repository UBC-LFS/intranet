from django.db import models
from modelcluster.fields import ParentalKey
from taggit.models import Tag, TaggedItemBase
from core.models import IndexModel, PageModel
from modelcluster.contrib.taggit import ClusterTaggableManager


class NewToLFSTag(TaggedItemBase):
    content_object = ParentalKey('NewToLFSPage', related_name='tagged_items', on_delete=models.CASCADE)

class NewToLFSPage(PageModel):
    tags = ClusterTaggableManager(through=NewToLFSTag, blank=True)
    parent_page_types = ['NewToLFSIndex']

class NewToLFSIndex(IndexModel):
    subpage_types = ['NewToLFSPage']