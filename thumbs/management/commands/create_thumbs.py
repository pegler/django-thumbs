from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from thumbs import ImageWithThumbsField, get_thumb_name, generate_thumb


class Command(BaseCommand):

    def handle(self, *args, **options):
        thumb_fields = []

        for content_type in ContentType.objects.all():
            model = content_type.model_class()
            if not model:  # in case of a stale ContentType
                continue

            for field in model._meta.fields:
                if isinstance(field, ImageWithThumbsField):
                    thumb_fields.append((model, field))

        for model, field in thumb_fields:
            attname = field.get_attname()
            for obj in model.objects.all():
                image = getattr(obj, attname)
                if not image.name:
                    continue

                sizes_to_generate = []
                storage = image.storage

                if not storage.exists(image.name):
                    continue

                for size in image.sizes:
                    width, height = size
                    thumb_name = get_thumb_name(image.name, width, height)

                    if not storage.exists(thumb_name):
                        sizes_to_generate.append(size)

                if sizes_to_generate:
                    image_file = image.file

                    ext = image.name.rsplit('.', 1)[1]
                    for size in sizes_to_generate:
                        width, height = size
                        thumb_content = generate_thumb(image_file, size, ext)
                        thumb_name = get_thumb_name(image.name, width, height)
                        image.storage.save(thumb_name, thumb_content)
