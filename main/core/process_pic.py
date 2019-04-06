import numpy
import imageio


class Image:
    def __init__(self, uri:str):
        self.data = imageio.imread(uri)

    def width(self) -> int:
        return self.data.shape[1]
    
    def height(self) -> int:
        return self.data.shape[0]

    
