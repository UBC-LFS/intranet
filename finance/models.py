from django.db import models
from modelcluster.fields import ParentalKey
from taggit.models import Tag, TaggedItemBase
from core.models import IndexModel, PageModel
from modelcluster.contrib.taggit import ClusterTaggableManager


class FinanceTag(TaggedItemBase):
    content_object = ParentalKey('FinancePage', related_name='tagged_items', on_delete=models.CASCADE)

class FinancePage(PageModel):
    tags = ClusterTaggableManager(through=FinanceTag, blank=True)
    parent_page_types = ['FinanceIndex']

class FinanceIndex(IndexModel):
    subpage_types = ['FinancePage']