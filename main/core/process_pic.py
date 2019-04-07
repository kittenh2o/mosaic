import numpy
import imageio


class Image:
    def __init__(self, uri:str):
        self.data = imageio.imread(uri)

    def width(self) -> int:
        return self.data.shape[1]
    
    def height(self) -> int:
        return self.data.shape[0]

    def size(self) -> int:
        return self.width()*self.height()

class ImageProcessor:
    def eval_rgb(self, image:Image) -> dict:
        r_sum = g_sum = b_sum = 0
        for col in image.data:
            for pixel in col:
                r_sum += pixel[0]
                g_sum += pixel[1]
                b_sum += pixel[2]
        
        r_avg, g_avg, b_avg = r_sum/image.size(), g_sum/image.size(), b_sum/image.size()

        return {
            "r": r_avg,
            "g": g_avg,
            "b": b_avg
        }

    def diff(self, image1:Image, image2:Image) -> int:
        rgb1 = self.eval_rgb(image1)
        rgb2 = self.eval_rgb(image2)

        return ((rgb1['r']-rgb2['r'])**2 + (rgb1['g']-rgb2['g'])**2 + (rgb1['b']-rgb2['b'])**2) 