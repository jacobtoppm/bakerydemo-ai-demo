from wagtail_content_import.mappers.streamfield import StreamFieldMapper
from wagtail_content_import.mappers.converters import RichTextConverter, ImageConverter, TableConverter, TextConverter, BaseConverter


class ImageBlockConverter(BaseConverter):
    image_converter = ImageConverter('block')

    def __call__(self, element, user, *args, **kwargs):
        image_block = self.image_converter(element, user, *args, **kwargs)
        return (self.block_name, {'show_full_image': None, 'image': image_block[1]})


class SimpleBreadMapper(StreamFieldMapper):
    html = RichTextConverter('paragraph')
    image = ImageBlockConverter('image')
    heading = TextConverter('heading')
    table = TableConverter('table')

