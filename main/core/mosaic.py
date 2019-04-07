from main.core.process_pic import Image, ImageProcessor
from main.core.tiles import TileResource
import numpy


class Mosaic:
    def __init__(self, uri: str):
        self.original_image = Image(uri)
        self.tile_library = TileResource()
        self.tile_size = (self.original_image.width() // 10, self.original_image.height() // 10)

    def add_tile(self, uri: str):
        self.tile_library.add_tile(Image(uri))

    def add_tiles(self, uris: list):
        for uri in uris:
            self.add_tile(uri)

    def transform(self, tile_size: tuple = None):
        if tile_size:
            self.tile_size = tile_size

        self.tile_library.prepare(self.tile_size)

        w, h = self.original_image.width(), self.original_image.height()
        diff_w, diff_h = w % self.tile_size[0], h % self.tile_size[1]

        if diff_w or diff_h:
            ImageProcessor.resize(image=self.original_image, size=(w + diff_w, h + diff_h))

    def find_best_tile(self, segment: Image) -> Image:
        min_ind = numpy.argmin(
            (ImageProcessor.diff_with_rgb(segment, rgb) for rgb in self.tile_library.tiles_rgb)
        )
        return self.tile_library.library[min_ind]

    def match(self) -> list:
        result = list()
        t_w, t_h = self.tile_size[0], self.tile_size[1]

        for w_start in range(0, self.original_image.width(), t_w):
            for h_start in range(0, self.original_image.height(), t_h):
                segment = Image(data=self.original_image.get_data()[w_start:w_start + t_w][h_start:h_start + t_h])
                matched_tile = self.find_best_tile(segment)
                result.append(matched_tile)

        return result
