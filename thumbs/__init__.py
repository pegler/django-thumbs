#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# -*- mode: python -*-
# vi: set ft=python :


""" django-thumbs

Improved by VanNoppen Marketing
Version 1.0.0

Original django-thumbs by Antonio Melé (http://django.es)
"""


from django.db.models import ImageField
from django.db.models.fields.files import ImageFieldFile
from django.core.files.base import ContentFile

from south.modelsinspector import add_introspection_rules
from PIL import Image
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO


def generate_thumb(img, thumb_size, format):
    img.seek(0)  # see http://code.djangoproject.com/ticket/8222 for details
    image = Image.open(img)

    # Convert to RGB if necessary
    if image.mode not in ('L', 'RGB'):
        image = image.convert('RGB')

    # get size
    thumb_w, thumb_h = thumb_size
    # If you want to generate a square thumbnail
    if thumb_w == thumb_h:
        # quad
        xsize, ysize = image.size
        # get minimum size
        minsize = min(xsize, ysize)
        # largest square possible in the image
        xnewsize = (xsize - minsize) / 2
        ynewsize = (ysize - minsize) / 2
        # crop it
        image2 = image.crop((xnewsize, ynewsize, xsize - xnewsize, ysize - ynewsize))
        # load is necessary after crop
        image2.load()
        # thumbnail of the cropped image (with ANTIALIAS to make it look better)
        image2.thumbnail(thumb_size, Image.ANTIALIAS)
    else:
        # not quad
        image2 = image
        image2.thumbnail(thumb_size, Image.ANTIALIAS)

    io = StringIO()
    # PNG and GIF are the same, JPG is JPEG
    if format.upper() == 'JPG':
        format = 'JPEG'

    image2.save(io, format)
    return ContentFile(io.getvalue())


def get_thumb_name(name, width, height):
    split = name.rsplit('.', 1)
    thumb_url = '%s.%sx%s.%s' % (split[0], width, height, split[1])
    return thumb_url


class ImageWithThumbsFieldFile(ImageFieldFile):
    """
    See ImageWithThumbsField for usage example
    """
    def __init__(self, *args, **kwargs):
        super(ImageWithThumbsFieldFile, self).__init__(*args, **kwargs)
        self.sizes = self.field.sizes

        if self.sizes and self.name:
            for width, height in self.sizes:
                setattr(self, 'url_%sx%s' % (width, height), get_thumb_name(self.url, width, height))

    def save(self, name, content, save=True):
        super(ImageWithThumbsFieldFile, self).save(name, content, save)

        if self.sizes:
            for size in self.sizes:
                split = self.name.rsplit('.', 1)

                width, height = size

                thumb_name = get_thumb_name(self.name, width, height)

                # you can use another thumbnailing function if you like
                thumb_content = generate_thumb(content, size, split[1])

                thumb_name_ = self.storage.save(thumb_name, thumb_content)

                if not thumb_name == thumb_name_:
                    raise ValueError('There is already a file named %s' % thumb_name)

    def delete(self, save=True):
        super(ImageWithThumbsFieldFile, self).delete(save)
        if self.sizes:
            for size in self.sizes:
                width, height = size

                thumb_name = get_thumb_name(self.name, width, height)

                try:
                    self.storage.delete(thumb_name)
                except:
                    pass


class ImageWithThumbsField(ImageField):
    attr_class = ImageWithThumbsFieldFile

    def __init__(self, verbose_name=None, name=None, width_field=None,
                 height_field=None, sizes=None, **kwargs):
        self.verbose_name = verbose_name
        self.name = name
        self.width_field = width_field
        self.height_field = height_field
        self.sizes = sizes
        super(ImageField, self).__init__(**kwargs)


add_introspection_rules(
    [([ImageWithThumbsField], [], {"sizes": ["sizes", {}]})],
    ["^thumbs\.ImageWithThumbsField"]
)
