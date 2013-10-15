# django-thumbs

This branch of django-thumbs adds several key features:
 - South support
 - A management command to create thumbnails of existing files.  Good if you switch to django-thumbs from a different system, or if you add a new sized thumbnail to the field.

In progress:
 - Full test coverage
 - Better documentation for use with collectstatic and an S3 storage backend

The original django-thumbs project you can find it on [Google Code][1].

[1]: http://code.google.com/p/django-thumbs/ "django-thumbs on Google Code"


## Requirements

Specific versions are untested but it has been known to work with fairly old
versions of all requirements.

  + Django
  + PIL/Pillow


## ImageWithThumbsField Usage

Add an ImageWithThumbsField to your model:

    photo = ImageWithThumbsField(upload_to='images', sizes=((125,125),(300,200),)

To retrieve image URL, exactly the same way as with ImageField:

    my_object.photo.url

To retrieve thumbnails URL's just add the size to it:

    my_object.photo.url_125x125
    my_object.photo.url_300x200
