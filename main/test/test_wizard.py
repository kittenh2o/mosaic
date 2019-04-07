import glob
from os.path import dirname, join
from unittest import TestCase

from main.core.wizard import Wizard

target_uri = join(dirname(__file__), "image_resources", "target.png")

red_uri = join(dirname(__file__), "image_resources", "red.png")
green_uri = join(dirname(__file__), "image_resources", "green.png")
blue_uri = join(dirname(__file__), "image_resources", "blue.png")
white_uri = join(dirname(__file__), "image_resources", "white.png")


class TestWizard(TestCase):
    def test_execute(self):
        wizard = Wizard(target_uri, [red_uri, green_uri, blue_uri])
        wizard.execute()

    def test_execute2(self):
        tile_uris = glob.glob(join(dirname(__file__), "image_resources", "*.*"))
        wizard = Wizard("https://res.cloudinary.com/dwf6x1ohn/image/upload/v1534347950/bgnppredgmslafb5pkpw.jpg",
                        tile_uris, tile_size=(10, 10))
        wizard.execute()