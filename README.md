# django-thumbs

[![Build Status](https://travis-ci.org/pegler/django-thumbs.png?branch=master)](https://travis-ci.org/pegler/django-thumbs)
[![Coverage Status](https://coveralls.io/repos/pegler/django-thumbs/badge.png)](https://coveralls.io/r/pegler/django-thumbs)

This fork of django-thumbs adds several key features:
 - South support
 - A management command to create thumbnails of existing files.  Good if you switch to django-thumbs from a different system, or if you add a new sized thumbnail to the field.

In progress:
 - Full test coverage
 - Better documentation for use with collectstatic and an S3 storage backend

The original project can be found on [Google Code][1].

[1]: http://code.google.com/p/django-thumbs/ "django-thumbs on Google Code"


## Requirements

Specific versions are untested but it has been known to work with fairly old
versions of all requirements.

  + Django
  + PIL/Pillow


## ImageWithThumbsField Usage

Add an ImageWithThumbsField field to your model:

    photo = ImageWithThumbsField(upload_to='images', sizes=((125,125),(300,200),)

You can retrieve the image URL exactly the same way as with ImageField:

    my_object.photo.url

Thumbnail URLs just have the size appended to it:

    my_object.photo.url_125x125
    my_object.photo.url_300x200
