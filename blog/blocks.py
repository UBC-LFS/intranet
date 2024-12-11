from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.contrib.typed_table_block.blocks import TypedTableBlock


class ImageBlock(blocks.StructBlock):
    image = ImageChooserBlock(required=True)
    caption = blocks.CharBlock(required=False, help_text="Optional")
    width = blocks.IntegerBlock(required=False, help_text="Optional. Width in pixels (e.g., 300)")
    height = blocks.IntegerBlock(required=False, help_text="Optional. Height in pixels (e.g., 300)")


# Accordion
class AccordionItemBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=True)
    content = blocks.RichTextBlock(required=True)

    class Meta:
        label = "Accordion item"


class AccordionBlock(blocks.StructBlock):
    accordion_id = blocks.CharBlock(
        required=True,
        help_text="Unique ID for the accordion (used for Bootstrap collapse functionality)"
    )

    items = blocks.ListBlock(AccordionItemBlock(), help_text="Accordion items")

    class Meta:
        template = "blocks/accordion.html"
        icon = "list-ul"
        label = "Accordion"


# Column
class ColumnBlock(blocks.StructBlock):
    width = blocks.ChoiceBlock(
        choices=[(str(i), f"{i}/12") for i in range(1, 13)],
        default='6',
        help_text="Set the width of this column (1 to 12)."
    )

    content = blocks.StreamBlock(
        [
            ('visual', blocks.RichTextBlock(required=False)),
            ('html', blocks.RawHTMLBlock()),
            ('image', ImageBlock())
        ],
        required=False,
        help_text="Add content to this column."
    )

    class Meta:
        template = "blocks/column.html"
        icon = "placeholder"
        label = "Column"


class ColumnsBlock(blocks.StructBlock):
    columns = blocks.ListBlock(ColumnBlock(), min_num=1, max_num=12)

    class Meta:
        template = "blocks/columns.html"
        icon = "grip"
        label = "Columns"


# Table

class CustomTableBlock(TypedTableBlock):
    visual = blocks.RichTextBlock()
    html = blocks.RawHTMLBlock()

    class Meta:
        template = "blocks/table.html"
        icon = "table"
        label = "Table"
