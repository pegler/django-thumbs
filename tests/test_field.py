from django.core.files import File as DjangoFile
from django.test.testcases import SimpleTestCase
from .models import Example
from PIL import Image
import os

class ImageWithThumbsFieldFileTest(SimpleTestCase):
    def test_thumbs(self):
        filename = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'test_image.png')
        obj = Example.objects.create(image=DjangoFile(open(filename)))

        #ensure the thumbails were created
        dirname = os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)), '../test/'))
        thumb1 = Image.open(dirname+'/test_image.50x50.png')
        width, height = thumb1.size
        self.assertEqual(width, 50)
        self.assertEqual(height, 50)
        
        thumb2 = Image.open(dirname+'/test_image.500x125.png')
        width, height = thumb2.size
        self.assertEqual(width, 359)
        self.assertEqual(height, 125)
        
        self.assertEqual(obj.image.url, 'test/test_image.png')
        self.assertEqual(obj.image.url_50x50, 'test/test_image.50x50.png')
        self.assertEqual(obj.image.url_500x125, 'test/test_image.500x125.png')
        
        obj.image.delete()
        
        self.assertFalse(os.path.isfile(dirname+'/test_image.png'))
        self.assertFalse(os.path.isfile(dirname+'/test_image.50x50.png'))
        self.assertFalse(os.path.isfile(dirname+'/test_image.500x125.png'))