from os.path import dirname, join, pardir
from os import makedirs
from tempfile import mktemp

import imageio

from main.core.mosaic import Mosaic


class Wizard:
    """ a wizard class for end user to leverage"""
    def __init__(self, target_uri, tiles_uris, tile_size: tuple = None):
        self.tile_size = tile_size
        self.mosaic = Mosaic(target_uri)
        self.mosaic.add_tiles(tiles_uris)

    def execute(self):
        new_image = self.mosaic.make_mosaic(self.tile_size)
        output_dir = join(dirname(__file__), pardir, pardir, "output")
        try:
            makedirs(output_dir)
        except Exception as exc:
            print(exc)

        filename = mktemp(dir=output_dir) + ".png"
        imageio.imwrite(filename, new_image.img)
