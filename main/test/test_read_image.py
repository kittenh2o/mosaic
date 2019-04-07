import sys
import unittest
from os.path import dirname, join

sys.path.insert(0, dirname(dirname(__file__)))
from core.process_pic import Image, ImageProcessor

class TestReadImage(unittest.TestCase):
    
    def test_read(self):
        uris = [
            "https://res.cloudinary.com/dwf6x1ohn/image/upload/v1534347950/bgnppredgmslafb5pkpw.jpg",
            "https://res.cloudinary.com/dwf6x1ohn/image/upload/v1534347979/wptzfdqidfnlyhgt3kti.jpg"
        ]

        sizes = [
            (540, 547),
            (259, 194)
        ]

        for (uri, size) in zip(uris, sizes):
            image = Image(uri)
            self.assertEqual(size[0], image.width())
            self.assertEqual(size[1], image.height())
            self.assertEqual(size[0]*size[1], image.size())


class TestImageProcessor(unittest.TestCase):

    def setUp(self):
        red_uri = join(dirname(__file__), "image_resources", "red.png")
        green_uri = join(dirname(__file__), "image_resources", "green.png")
        blue_uri = join(dirname(__file__), "image_resources", "blue.png")

        self.red_image, self.green_image, self.blue_image = Image(red_uri), Image(green_uri), Image(blue_uri)
        

    def test_eval_image(self):
        self.assertEqual(ImageProcessor().eval_rgb(self.red_image)["r"], 255)
        self.assertEqual(ImageProcessor().eval_rgb(self.green_image)["g"], 255)
        self.assertEqual(ImageProcessor().eval_rgb(self.blue_image)["b"], 255)

    def test_image_diff(self):
        self.assertEqual(ImageProcessor().diff(self.red_image, self.blue_image), 2*255**2)

if __name__ == "__main__":
    suites = [unittest.TestLoader().loadTestsFromTestCase(TestClass) for TestClass in [TestImageProcessor, TestReadImage]]
    for suite in suites:
        unittest.TextTestRunner(verbosity=2).run(suite)