from unittest import TestCase
from main.core.wizard import Wizard
from os.path import dirname, join


target_uri = join(dirname(__file__), "image_resources", "target.png")
red_uri = join(dirname(__file__), "image_resources", "red.png")
green_uri = join(dirname(__file__), "image_resources", "green.png")
blue_uri = join(dirname(__file__), "image_resources", "blue.png")


class TestWizard(TestCase):
    def test_execute(self):
        wizard = Wizard(target_uri, [red_uri, green_uri, blue_uri])
        wizard.execute()
