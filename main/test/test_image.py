import unittest

from main.core.process_pic import Image


class TestImage(unittest.TestCase):

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
            self.assertEqual(size[0] * size[1], image.size())


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestImage)
    unittest.TextTestRunner(verbosity=2).run(suite)
