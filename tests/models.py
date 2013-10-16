from django.db import models
import thumbs

class Example(models.Model):
    image = thumbs.ImageWithThumbsField(upload_to='test', sizes=((50, 50), (500, 125), ))