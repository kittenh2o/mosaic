import glob
from os.path import dirname, join

from main.core.wizard import Wizard


local_resource_folder = join(dirname(__file__), "main", "test", "image_resources")

# Add local jpg and png files
tiles_uris = list(glob.glob(join(local_resource_folder, "*.jpg")))
tiles_uris.extend(list(glob.glob(join(local_resource_folder, ".png"))))

# Original image
target_uri = "https://res.cloudinary.com/dwf6x1ohn/image/upload/v1534347950/bgnppredgmslafb5pkpw.jpg"


if __name__ == "__main__":
    wizard = Wizard(target_uri=target_uri, tiles_uris=tiles_uris, tile_size=(10, 10))
    wizard.execute()
