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
from PIL import Image, ExifTags
try:  # pragma: nocover
    try:  # python 2
        from cStringIO import StringIO
    except ImportError:
        from StringIO import StringIO
except ImportError:  # pragma: nocover
    from io import StringIO  # python 3


# From: https://gist.github.com/olooney/1601455
class Size(object):
    def __init__(self, pair):
        self.width = float(pair[0])
        self.height = float(pair[1])

    @property
    def aspect_ratio(self):
        return self.width / self.height

    @property
    def size(self):
        return flat(self.width, self.height)

def flat( *nums ):
    'Build a tuple of ints from float or integer arguments. Useful because PIL crop and resize require integer points.'
    return tuple( int(round(n)) for n in nums )

def generate_thumb(img, thumb_size):
    img.seek(0)  # see http://code.djangoproject.com/ticket/8222 for details
    image = Image.open(img)
    orientation = None
    for _orientation in ExifTags.TAGS.keys():
        if ExifTags.TAGS[_orientation] == 'Orientation':
            orientation = _orientation
    try:
        exif = dict(image._getexif().items())
    except AttributeError:
        pass
    else:
        if orientation:
            if exif.get(orientation) == 3:
                image = image.rotate(180, expand=True)
            elif exif.get(orientation) == 6:
                image = image.rotate(270, expand=True)
            elif exif.get(orientation) == 8:
                image = image.rotate(90, expand=True)
    # Convert to RGB if necessary
    if image.mode not in ('L', 'RGB', 'RGBA'):
        image = image.convert('RGB')
    original = Size(image.size)
    target = Size(thumb_size)
    if target.aspect_ratio > original.aspect_ratio:
        # image is too tall: take some off the top and bottom
        scale_factor = target.width / original.width
        crop_size = Size( (original.width, target.height / scale_factor) )
        top_cut_line = (original.height - crop_size.height) / 2
        image = image.crop( flat(0, top_cut_line, crop_size.width, top_cut_line + crop_size.height) )
    elif target.aspect_ratio < original.aspect_ratio:
        # image is too wide: take some off the sides
        scale_factor = target.height / original.height
        crop_size = Size( (target.width/scale_factor, original.height) )
        side_cut_line = (original.width - crop_size.width) / 2
        image = imgage.crop( flat(side_cut_line, 0,  side_cut_line + crop_size.width, crop_size.height) )
    io = StringIO()
    format = image.format or 'jpeg'
    info = image.info
    image.save(io, format, **info)
    return ContentFile(io.getvalue())


def get_thumb_name(name, width, height):
    split = name.rsplit('.', 1)
    if len(split) == 2:
        thumb_url = '%s.%sx%s.%s' % (split[0], width, height, split[1])
    else:
        thumb_url = '%s.%sx%s' % (split[0], width, height)
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
                width, height = size

                thumb_name = get_thumb_name(self.name, width, height)

                # you can use another thumbnailing function if you like
                thumb_content = generate_thumb(content, size)

                thumb_name_ = self.storage.save(thumb_name, thumb_content)

                if not thumb_name == thumb_name_:
                    raise ValueError('There is already a file named %s' % thumb_name)

    def delete(self, save=True):
        if self.sizes:
            for size in self.sizes:
                width, height = size

                thumb_name = get_thumb_name(self.name, width, height)

                try:
                    self.storage.delete(thumb_name)
                except:
                    pass
        super(ImageWithThumbsFieldFile, self).delete(save)


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
