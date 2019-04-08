from main.core.process_pic import ImageProcessor, Image
from multiprocessing.dummy import Pool


class TileResource:
    """ A resource class to store all tiles"""
    def __init__(self, images=None):
        if images is None:
            images = list()
        self.library = images
        self.tiles_rgb = None
        self.tile_size = None

    def add_tile(self, image: Image):
        self.library.append(image)

    def _resize_and_calc_rgb(self, image: Image) -> dict:
        ImageProcessor.resize(image, self.tile_size)
        return ImageProcessor.eval_rgb(image)

    def prepare(self, target_size: tuple):
        """ prepare tile resources"""
        self.tile_size = target_size

        with Pool(4) as pool:
            results = pool.map(self._resize_and_calc_rgb, self.library)

        self.tiles_rgb = results


