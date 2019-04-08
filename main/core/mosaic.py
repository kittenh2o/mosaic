import logging
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool

import numpy

from main.core.process_pic import Image, ImageProcessor, Component
from main.core.tiles import TileResource


class Mosaic:
    """ Main module for converting image into mosaic"""
    def __init__(self, uri: str):
        self.original_image = Image(uri)
        self.tile_library = TileResource()
        self.tile_size = (self.original_image.width() // 10, self.original_image.height() // 10)

    def add_tile(self, uri: str):
        self.tile_library.add_tile(Image(uri))

    def add_tiles(self, uris: list):
        with ThreadPool(4) as pool:
            pool.map(self.add_tile, uris)

    def _prepare_resources(self, tile_size: tuple = None):
        """ enlarge/shrink tiles to the given or default size and adjust original image accordingly"""
        if tile_size:
            self.tile_size = tile_size

        self.tile_library.prepare(self.tile_size)

        w, h = self.original_image.width(), self.original_image.height()
        diff_w, diff_h = w % self.tile_size[0], h % self.tile_size[1]

        if diff_w or diff_h:
            new_w = w - diff_w + self.tile_size[0]
            new_h = h - diff_h + self.tile_size[1]
            ImageProcessor.resize(image=self.original_image, size=(new_w, new_h))

    def _find_best_tile(self, segment: Image) -> Image:
        """ find the best fitted tile to the given segment of image"""
        min_ind = numpy.argmin(
            [ImageProcessor.diff_with_rgb(segment, rgb) for rgb in self.tile_library.tiles_rgb]
        )

        return self.tile_library.library[min_ind]

    def _get_component(self, segment: Image, w_start: int, h_start: int):
        # print("Process {0}:: get_component".format(os.getpid()))
        return Component(image=self._find_best_tile(segment), w_start=w_start, h_start=h_start)

    def _match_and_create(self) -> None:
        """ match original image with tiles"""
        t_w, t_h = self.tile_size[0], self.tile_size[1]

        nw = self.original_image.width()//t_w
        nh = self.original_image.height()//t_h

        with Pool(processes=4) as pool:
            results = list()
            for i in range(nw):
                for j in range(nh):
                    w_start, h_start = i * t_w, j * t_h
                    segment = Image(data=self.original_image.img[h_start:h_start + t_h, w_start:w_start + t_w])
                    res = pool.apply_async(self._get_component, (segment, w_start, h_start))
                    results.append(res)

            components = [x.get() for x in results]
        logging.log(logging.DEBUG, "match finished")

        for component in components:
            ImageProcessor.replace(self.original_image, component)

        logging.log(logging.DEBUG, "_match_and_create finished")

    def make_mosaic(self, tile_size: tuple = None) -> Image:
        """ Interface for users to call"""
        self._prepare_resources(tile_size)
        self._match_and_create()
        return self.original_image
