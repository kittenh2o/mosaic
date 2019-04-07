import numpy

from main.core.process_pic import Image, ImageProcessor, Component
from main.core.tiles import TileResource


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

    def prepare_resources(self, tile_size: tuple = None):
        if tile_size:
            self.tile_size = tile_size

        self.tile_library.prepare(self.tile_size)

        w, h = self.original_image.width(), self.original_image.height()
        diff_w, diff_h = w % self.tile_size[0], h % self.tile_size[1]

        if diff_w or diff_h:
            new_w = w - diff_w + self.tile_size[0]
            new_h = h - diff_h + self.tile_size[1]
            ImageProcessor.resize(image=self.original_image, size=(new_w, new_h))

    def find_best_tile(self, segment: Image) -> Image:
        min_ind = numpy.argmin(
            [ImageProcessor.diff_with_rgb(segment, rgb) for rgb in self.tile_library.tiles_rgb]
        )

        return self.tile_library.library[min_ind]

    def match(self) -> list:
        result = list()
        t_w, t_h = self.tile_size[0], self.tile_size[1]

        nw = self.original_image.width()//t_w
        nh = self.original_image.height()//t_h

        for i in range(nw):
            for j in range(nh):
                w_start, h_start = i * t_w, j * t_h
                segment = Image(data=self.original_image.img[h_start:h_start + t_h, w_start:w_start + t_w])
                matched_tile = self.find_best_tile(segment)
                result.append(Component(image=matched_tile, w_start=w_start, h_start=h_start))

        return result

    def create(self, components: list) -> Image:
        for component in components:
            ImageProcessor.replace(self.original_image, component)

        return self.original_image

    def make_mosaic(self, tile_size: tuple = None):
        self.prepare_resources(tile_size)
        components = self.match()
        return self.create(components)