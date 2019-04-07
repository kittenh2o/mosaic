import imageio
import cv2.cv2 as cv2


class Image:
    def __init__(self, uri: str = None, data=None):
        self.img = None
        self._uri = uri

        if uri:
            self.img = imageio.imread(uri)
        elif data is not None:
            self.img = data

    def reload(self, data=None):
        if self._uri:
            self.img = imageio.imread(self._uri)
        elif data is not None:
            self.img = data
        else:
            raise KeyError

    def width(self) -> int:
        return self.img.shape[1]

    def height(self) -> int:
        return self.img.shape[0]

    def size(self) -> int:
        return self.width() * self.height()


class Component:
    def __init__(self, image: Image, w_start: int, h_start: int):
        self.image = image
        self.w_start = w_start
        self.h_start = h_start


class ImageProcessor:
    @classmethod
    def eval_rgb(cls, image: Image) -> dict:
        r_sum = g_sum = b_sum = 0
        for col in image.img:
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
        rgb2 = cls.eval_rgb(image2)

        return cls.diff_with_rgb(image1, rgb2)

    @classmethod
    def diff_with_rgb(cls, image: Image, rgb: dict) -> int:
        calc_res = cls.eval_rgb(image)

        return (calc_res['r'] - rgb['r']) ** 2 + (calc_res['g'] - rgb['g']) ** 2 + (calc_res['b'] - rgb['b']) ** 2

    @classmethod
    def resize(cls, image: Image, size: tuple = None, ratio: tuple = None) -> None:
        if size is not None:
            if size[0] < image.width() and size[1] < image.height():
                interp_strategy = cv2.INTER_AREA
            else:
                interp_strategy = cv2.INTER_CUBIC
            image.img = cv2.resize(src=image.img, dsize=size, interpolation=interp_strategy)

        elif ratio is not None:
            if ratio[0] < 1.0 and ratio[1] < 1.0:
                interp_strategy = cv2.INTER_AREA
            else:
                interp_strategy = cv2.INTER_CUBIC
            image.img = cv2.resize(src=image.img, dsize=(0, 0), fx=ratio[0], fy=ratio[1], interpolation=interp_strategy)

        else:
            raise KeyError

    @classmethod
    def replace(cls, image: Image, component: Component):
        h_start = component.h_start
        h_end = h_start + component.image.height()
        w_start = component.w_start
        w_end = w_start + component.image.width()

        image.img[h_start:h_end, w_start:w_end, 0:3] = component.image.img[:, :, 0:3]