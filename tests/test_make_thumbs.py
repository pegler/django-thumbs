from django.core.files import File as DjangoFile
from django.test.testcases import SimpleTestCase
from .models import Example
from PIL import Image
import os
from django.core.management import call_command

class MakeThumbsManagementCommandTestCase(SimpleTestCase):
    def test_make_thumbs(self):
        filename = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'test_image.png')
        obj = Example.objects.create(image=DjangoFile(open(filename)))

        #ensure the thumbails were created
        dirname = os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)), '../test/'))
        
        image_field = Example._meta.get_field('image')
        image_field.sizes = image_field.sizes+((100,100),)
        
        call_command('create_thumbs')
        
        thumb1 = Image.open(dirname+'/test_image.100x100.png')
        width, height = thumb1.size
        self.assertEqual(width, 100)
        self.assertEqual(height, 100)
        
        obj.image.delete()