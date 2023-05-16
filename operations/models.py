from django.db import models
from modelcluster.fields import ParentalKey
from taggit.models import Tag, TaggedItemBase
from core.models import IndexModel, PageModel
from modelcluster.contrib.taggit import ClusterTaggableManager


class OperationTag(TaggedItemBase):
    content_object = ParentalKey('OperationPage', related_name='tagged_items', on_delete=models.CASCADE)

class OperationPage(PageModel):
    tags = ClusterTaggableManager(through=OperationTag, blank=True)
    parent_page_types = ['OperationsIndex']

class OperationsIndex(IndexModel):
    subpage_types = ['OperationPage']