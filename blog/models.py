from django.conf import settings
from django.db import models
from wagtail import blocks
from wagtail.models import Page
from wagtail.fields import StreamField, RichTextField
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel, HelpPanel
from wagtail.search import index
from wagtail.images.blocks import ImageChooserBlock
from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase
from wagtail.contrib.routable_page.models import RoutablePageMixin
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.contrib.forms.panels import FormSubmissionsPanel

from django.core.mail import send_mail
import smtplib
from email.mime.text import MIMEText

from datetime import date
from slugify import slugify

from .blocks import AccordionBlock, ColumnsBlock, CustomTableBlock
from core.functions import *


class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey('BlogPage', related_name='tagged_items', on_delete=models.CASCADE)


class BlogPostTag(TaggedItemBase):
    content_object = ParentalKey('BlogPost', related_name='tagged_items', on_delete=models.CASCADE)


class BlogPost(Page):
    publish_date = models.DateField('Publish date', blank=True, null=True)
    
    body = StreamField([
        ('visual', blocks.RichTextBlock(features=settings.RICH_TEXT_FEATURES)),
        ('html', blocks.RawHTMLBlock()),
        ('image', ImageChooserBlock()),
        ('accordion', AccordionBlock()),
        ('columns', ColumnsBlock()),
        ('table', CustomTableBlock())
    ], use_json_field=True, blank=True)

    tags = ClusterTaggableManager(through=BlogPostTag, blank=True)

    search_fields = Page.search_fields + [
        index.SearchField('body')
    ]

    content_panels = Page.content_panels + [
        FieldPanel('publish_date'),
        FieldPanel('body'),
        FieldPanel('tags')
    ]
    
    parent_page_types = ['blog.BlogPage']
    subpage_types = []

    def get_context(self, request):
        context = super(BlogPost, self).get_context(request)
        context['model_name'] = self._meta.model_name
        context['sidebar_menu'] = make_sidebar_menu(request, get_user_groups(request), self.get_parent().get_parent())
        return context

    @property
    def get_tags(self):
        tags = self.tags.all()
        for tag in tags:
            tag.url = f'/search/?query={tag.slug}&method=tag&page=1'
        return tags


class BlogPage(Page):
    publish_date = models.DateField('Publish date', blank=True, null=True)
    body = StreamField([
        ('visual', blocks.RichTextBlock(features=settings.RICH_TEXT_FEATURES)),
        ('html', blocks.RawHTMLBlock()),
        ('image', ImageChooserBlock()),
        ('accordion', AccordionBlock()),
        ('columns', ColumnsBlock()),
        ('table', CustomTableBlock())
    ], use_json_field=True, blank=True)

    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)

    search_fields = Page.search_fields + [
        index.SearchField('body')
    ]

    content_panels = Page.content_panels + [
        FieldPanel('publish_date'),
        FieldPanel('body'),
        FieldPanel('tags')
    ]

    parent_page_types = ['blog.BlogIndex']
    subpage_types = ['blog.BlogPost', 'blog.FormPost']

    def get_context(self, request):
        context = super(BlogPage, self).get_context(request)
        context['model_name'] = self._meta.model_name
        context['sidebar_menu'] = make_sidebar_menu(request, get_user_groups(request), self.get_parent())
        return context

    @property
    def get_tags(self):
        tags = self.tags.all()
        for tag in tags:
            tag.url = f"/search/?query={tag.slug}&method=tag&page=1"
        return tags


class BlogIndex(RoutablePageMixin, Page):
    publish_date = models.DateField('Publish date', blank=True, null=True)
    body = StreamField([
        ('visual', blocks.RichTextBlock(features=settings.RICH_TEXT_FEATURES)),
        ('html', blocks.RawHTMLBlock()),
        ('image', ImageChooserBlock()),
        ('accordion', AccordionBlock()),
        ('columns', ColumnsBlock()),
        ('table', CustomTableBlock())
    ], use_json_field=True, blank=True)

    search_fields = Page.search_fields + [
        index.SearchField('body')
    ]

    content_panels = Page.content_panels + [
        FieldPanel('publish_date'),
        FieldPanel('body')
    ]

    subpage_types = ['blog.BlogPage', 'blog.FormPage']

    def get_context(self, request):
        context = super(BlogIndex, self).get_context(request)
        context['model_name'] = self._meta.model_name
        context['sidebar_menu'] = make_sidebar_menu(request, get_user_groups(request), self)
        return context
    

# Form


from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox


class FormField(AbstractFormField):
    page = ParentalKey('FormIndex', on_delete=models.CASCADE, related_name='form_fields')


class FormIndex(AbstractEmailForm):
    publish_date = models.DateField('Publish Date', blank=True, null=True)
    intro = RichTextField(blank=True)
    thank_you_text = RichTextField(verbose_name="Thank You Text", blank=True)
    from_address = models.CharField(max_length=255, verbose_name="Sender Email Address", blank=True)
    to_address = models.CharField(max_length=255, verbose_name="Recipient Email Address", help_text="Separate multiple email addresses with commas.", blank=True)
    subject = models.CharField(max_length=255, verbose_name="Email Subject", blank=True)

    content_panels = AbstractEmailForm.content_panels + [
        FormSubmissionsPanel(),
        FieldPanel('publish_date'),
        FieldPanel('intro'),
        InlinePanel('form_fields', label="Form Fields"),
        FieldPanel('thank_you_text'),
        MultiFieldPanel([
            HelpPanel(content="Note: <br /> 1. Please use 'Email' if you would like to add an email address to a form, and it will be used as the sender email address. <br /> 2. If the sender email address is empty, no-reply@landfood.ubc.ca will be used as the default email address."),
            FieldPanel('from_address'),
            FieldPanel('to_address'),
            FieldPanel('subject'),
        ], "Admin - Email Notification (Optional)"),
    ]

    def get_form_class(self):
        form_class = super().get_form_class()
        class CustomForm(form_class):
            captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())
        return CustomForm

    def get_context(self, request):
        context = super(FormIndex, self).get_context(request)
        context['model_name'] = self._meta.model_name
        context['sidebar_menu'] = make_sidebar_menu(request, get_user_groups(request), self)
        return context

    def send_mail(self, form):
        sender = None
        user_address = form.cleaned_data.get('email', None)
        
        if user_address:
            sender = user_address
        elif self.from_address:
            sender = self.from_address
        else:
            sender = settings.EMAIL_FROM

        if sender and self.to_address and self.subject:
            fields = ''
            for field in self.render_email(form).split('\n'):            
                if field:
                    field = field.replace('\r', '')
                    key = slugify(field.split(':')[0]).replace('-', '_')
                    if key != 'captcha':
                        if key in list(form.fields.keys()):
                            fields += '<li>' + field + '</li>'
                        else:
                            fields = fields[:-5] + ' ' + field + '</li>'
            
            for receiver in self.to_address.split(','):
                message = '''\
                <div>
                    <p>Dear {0},</p>
                    <p>A new form has been submitted. Please review the details and process the request accordingly.
                    <h5>Form Details</h5>
                    <ul>{1}</ul>
                    <p>Best regards,</p>
                    <p>LFS Intranet</p>
                </div>
                '''.format(receiver.strip(), fields)

                msg = MIMEText(message, 'html')
                msg['Subject'] = '{0} - {1}'.format(self.subject, date.today().strftime('%x'))
                msg['From'] = sender
                msg['To'] = receiver.strip()

                try:
                    server = smtplib.SMTP(settings.EMAIL_HOST)
                    server.sendmail(sender, receiver, msg.as_string())
                    print(f'The sender, {sender}: an email has been sent to {receiver.strip()}')
                except Exception as e:
                    print('Send Email Error:', e)
                finally:
                    server.quit()


class FormPage(FormIndex):
    template = "blog/form_page.html"
    parent_page_types = ['blog.BlogIndex']
    subpage_types = []

    def get_context(self, request):
        context = super(FormPage, self).get_context(request)
        context['model_name'] = self._meta.model_name
        context['sidebar_menu'] = make_sidebar_menu(request, get_user_groups(request), self.get_parent())
        return context


class FormPost(FormIndex):
    template = "blog/form_post.html"
    parent_page_types = ['blog.BlogPage']
    subpage_types = []

    def get_context(self, request):
        context = super(FormPost, self).get_context(request)
        context['model_name'] = self._meta.model_name
        context['sidebar_menu'] = make_sidebar_menu(request, get_user_groups(request), self.get_parent().get_parent())
        return context
