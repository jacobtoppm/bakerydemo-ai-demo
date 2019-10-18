from wagtail_content_import.mappers.streamfield import StreamFieldMapper
from wagtail_content_import.mappers.converters import RichTextConverter, ImageConverter, TableConverter, TextConverter

class SimpleBreadMapper(StreamFieldMapper):
    html = RichTextConverter('paragraph')
    image = ImageConverter('image')
    heading = TextConverter('heading')
    table = TableConverter('table')
