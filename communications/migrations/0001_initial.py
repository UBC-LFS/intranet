# Generated by Django 4.1.9 on 2023-05-15 23:28

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.contrib.taggit
import modelcluster.fields
import wagtail.blocks
import wagtail.contrib.routable_page.models
import wagtail.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailcore', '0083_workflowcontenttype'),
        ('taggit', '0005_auto_20220424_2025'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommunicationPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('publish_date', models.DateField(blank=True, null=True, verbose_name='Publish date')),
                ('body', wagtail.fields.StreamField([('visual', wagtail.blocks.RichTextBlock(features=['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'bold', 'italic', 'ol', 'ul', 'hr', 'link', 'document-link', 'image', 'embed', 'code', 'superscript', 'subscript', 'strikethrough', 'blockquote'])), ('html', wagtail.blocks.RawHTMLBlock()), ('image', wagtail.images.blocks.ImageChooserBlock())], blank=True, use_json_field=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='CommunicationsIndex',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('publish_date', models.DateField(blank=True, null=True, verbose_name='Publish date')),
                ('body', wagtail.fields.StreamField([('visual', wagtail.blocks.RichTextBlock(features=['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'bold', 'italic', 'ol', 'ul', 'hr', 'link', 'document-link', 'image', 'embed', 'code', 'superscript', 'subscript', 'strikethrough', 'blockquote'])), ('html', wagtail.blocks.RawHTMLBlock()), ('image', wagtail.images.blocks.ImageChooserBlock())], blank=True, use_json_field=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(wagtail.contrib.routable_page.models.RoutablePageMixin, 'wagtailcore.page'),
        ),
        migrations.CreateModel(
            name='CommunicationTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_object', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='tagged_items', to='communications.communicationpage')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_items', to='taggit.tag')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='communicationpage',
            name='tags',
            field=modelcluster.contrib.taggit.ClusterTaggableManager(blank=True, help_text='A comma-separated list of tags.', through='communications.CommunicationTag', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]
