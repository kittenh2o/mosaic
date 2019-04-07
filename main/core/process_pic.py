import imageio
import cv2.cv2 as cv2


class Image:
    def __init__(self, uri: str):
        self.__img = imageio.imread(uri)

    def get_data(self):
        return self.__img

    def set_data(self, data):
        self.__img = data

    def width(self) -> int:
        return self.__img.shape[1]

    def height(self) -> int:
        return self.__img.shape[0]

    def size(self) -> int:
        return self.width() * self.height()


class ImageProcessor:
    @classmethod
    def eval_rgb(cls, image: Image) -> dict:
        r_sum = g_sum = b_sum = 0
        for col in image.get_data():
            for pixel in col:
                r_sum += pixel[0]
                g_sum += pixel[1]
                b_sum += pixel[2]

        r_avg, g_avg, b_avg = r_sum / image.size(), g_sum / image.size(), b_sum / image.size()

        return {
            "r": r_avg,
            "g": g_avg,
            "b": b_avg
        }

    @classmethod
    def diff(cls, image1: Image, image2: Image) -> int:
        rgb1 = cls.eval_rgb(image1)
        rgb2 = cls.eval_rgb(image2)

        return (rgb1['r'] - rgb2['r']) ** 2 + (rgb1['g'] - rgb2['g']) ** 2 + (rgb1['b'] - rgb2['b']) ** 2

    @classmethod
    def resize(cls, image: Image, size: tuple = None, ratio: tuple = None) -> None:
        if size is not None:
            if size[0] < image.width() and size[1] < image.height():
                interp_strategy = cv2.INTER_AREA
            else:
                interp_strategy = cv2.INTER_CUBIC
            image.set_data(cv2.resize(src=image.get_data(), dsize=size, interpolation=interp_strategy))

        elif ratio is not None:
            if ratio[0] < 1.0 and ratio[1] < 1.0:
                interp_strategy = cv2.INTER_AREA
            else:
                interp_strategy = cv2.INTER_CUBIC
            image.set_data(cv2.resize(src=image.get_data(), dsize=(0, 0), fx=ratio[0], fy=ratio[1], interpolation=interp_strategy))

        else:
            raise KeyError

class Tiles:
    def __init__(self, images: list):
        pass

    def resize(self, image: Image):
        pass
