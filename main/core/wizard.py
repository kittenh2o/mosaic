from os.path import dirname, join, pardir
from tempfile import mktemp

import imageio

from main.core.mosaic import Mosaic


class Wizard:
    def __init__(self, target_uri, tiles_uris, tile_size: tuple = None):
        self.tile_size = tile_size
        self.mosaic = Mosaic(target_uri)
        self.mosaic.add_tiles(tiles_uris)

    def execute(self):
        new_image = self.mosaic.make_mosaic(self.tile_size)
        filename = mktemp(dir=join(dirname(__file__), pardir, pardir, "output")) + ".png"
        imageio.imwrite(filename, new_image.img)
