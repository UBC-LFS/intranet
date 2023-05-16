from django.db import models
from modelcluster.fields import ParentalKey
from taggit.models import Tag, TaggedItemBase
from core.models import IndexModel, PageModel
from modelcluster.contrib.taggit import ClusterTaggableManager


class FacultyResourceTag(TaggedItemBase):
    content_object = ParentalKey('FacultyResourcePage', related_name='tagged_items', on_delete=models.CASCADE)

class FacultyResourcePage(PageModel):
    tags = ClusterTaggableManager(through=FacultyResourceTag, blank=True)
    parent_page_types = ['FacultyResourcesIndex']

class FacultyResourcesIndex(IndexModel):
    subpage_types = ['FacultyResourcePage']