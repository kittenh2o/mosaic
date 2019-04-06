import sys
import unittest
from os.path import dirname

sys.path.insert(0, dirname(dirname(__file__)))
from core.process_pic import Image

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


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestReadImage)
    unittest.TextTestRunner().run(suite)