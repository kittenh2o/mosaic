from main.core.process_pic import ImageProcessor, Image


class TileResource:
    ''' A resource class to store all tiles'''
    def __init__(self, images=None):
        if images is None:
            images = list()
        self.library = images
        self.tiles_rgb = list()

    def add_tile(self, image: Image):
        self.library.append(image)

    def prepare(self, target_size: tuple):
        ''' prepare tile resources'''
        for image in self.library:
            ImageProcessor.resize(image, target_size)

        self._calc_tiles_rgb()

    def _calc_tiles_rgb(self):
        ''' calcuate rgb dict for all tiles'''
        self.tiles_rgb = [
            ImageProcessor.eval_rgb(image) for image in self.library
        ]



