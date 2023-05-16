from django.db import models
from modelcluster.fields import ParentalKey
from taggit.models import Tag, TaggedItemBase
from core.models import IndexModel, PageModel
from modelcluster.contrib.taggit import ClusterTaggableManager


class PolicyTag(TaggedItemBase):
    content_object = ParentalKey('PolicyPage', related_name='tagged_items', on_delete=models.CASCADE)

class PolicyPage(PageModel):
    tags = ClusterTaggableManager(through=PolicyTag, blank=True)
    parent_page_types = ['PoliciesIndex']

class PoliciesIndex(IndexModel):
    subpage_types = ['PolicyPage']