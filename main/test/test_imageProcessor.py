from unittest import TestCase
from os.path import dirname, join

from main.core.process_pic import Image, ImageProcessor


class TestImageProcessor(TestCase):

    def setUp(self):
        red_uri = join(dirname(__file__), "image_resources", "red.png")
        green_uri = join(dirname(__file__), "image_resources", "green.png")
        blue_uri = join(dirname(__file__), "image_resources", "blue.png")

        self.red_image, self.green_image, self.blue_image = Image(
            red_uri), Image(green_uri), Image(blue_uri)

    def test_eval_rgb(self):
        self.assertEqual(ImageProcessor().eval_rgb(self.red_image)["r"], 255)
        self.assertEqual(ImageProcessor().eval_rgb(self.green_image)["g"], 255)
        self.assertEqual(ImageProcessor().eval_rgb(self.blue_image)["b"], 255)

    def test_diff(self):
        self.assertEqual(ImageProcessor().diff(
            self.red_image, self.blue_image), 2 * 255 ** 2)

    def test_resize(self):
        uri = join(dirname(__file__), "image_resources", "red.png")
        image = Image(uri)
        w_original = image.width()
        h_original = image.height()

        # Shrink size
        ImageProcessor.resize(image, ratio=(0.5, 0.8))
        self.assertEqual(image.width(), w_original*0.5)
        self.assertEqual(image.height(), h_original*0.8)

        # Enlarge size
        image = Image(uri)
        ImageProcessor.resize(image, size=(1024, 768))
        self.assertEqual(image.width(), 1024)
        self.assertEqual(image.height(), 768)


