from django.db import models
from modelcluster.fields import ParentalKey
from taggit.models import Tag, TaggedItemBase
from core.models import IndexModel, PageModel
from modelcluster.contrib.taggit import ClusterTaggableManager


class AboutTag(TaggedItemBase):
    content_object = ParentalKey('AboutPage', related_name='tagged_items', on_delete=models.CASCADE)

class AboutPage(PageModel):
    tags = ClusterTaggableManager(through=AboutTag, blank=True)
    parent_page_types = ['AboutIndex']

class AboutIndex(IndexModel):
    subpage_types = ['AboutPage']
