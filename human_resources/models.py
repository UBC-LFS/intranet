from django.db import models
from modelcluster.fields import ParentalKey
from taggit.models import Tag, TaggedItemBase
from core.models import IndexModel, PageModel
from modelcluster.contrib.taggit import ClusterTaggableManager


class HumanResourceTag(TaggedItemBase):
    content_object = ParentalKey('HumanResourcePage', related_name='tagged_items', on_delete=models.CASCADE)

class HumanResourcePage(PageModel):
    tags = ClusterTaggableManager(through=HumanResourceTag, blank=True)
    parent_page_types = ['HumanResourcesIndex']

class HumanResourcesIndex(IndexModel):
    subpage_types = ['HumanResourcePage']