import errno
import os
import functools
from PIL import Image

from common.common.service import picture


class PictureService(picture.PictureService):
    def __init__(self, config):
        self.config = config

    @staticmethod
    def _image_transpose_exif(im):
        """
        Applies EXIF transformations to `im` (if present) and returns
        the result as a new image.
        Taken from [here](https://stackoverflow.com/a/30462851/1667018)
        and adapted.
        """
        exif_orientation_tag = 0x0112  # contains an integer, 1 through 8
        exif_transpose_sequences = [  # corresponding to the following
            [],
            [Image.FLIP_LEFT_RIGHT],
            [Image.ROTATE_180],
            [Image.FLIP_TOP_BOTTOM],
            [Image.FLIP_LEFT_RIGHT, Image.ROTATE_90],
            [Image.ROTATE_270],
            [Image.FLIP_TOP_BOTTOM, Image.ROTATE_90],
            [Image.ROTATE_90],
        ]

        try:
            seq = exif_transpose_sequences[
                im._getexif()[exif_orientation_tag] - 1
            ]
        except Exception:
            return im
        else:
            if seq:
                return functools.reduce(
                    lambda im, op: im.transpose(op), seq, im
                )
            else:
                return im

    def _process_image_from_config(self, picture, config):
        def new_img(size, im_to_paste=None):
            im = Image.new(
                "RGB",
                (
                    min(size[0], im_to_paste.size[0]),
                    min(size[1], im_to_paste.size[1])
                )
            )
            im.paste(
                im_to_paste,
                (
                    min(0, (size[0] - im_to_paste.size[0]) // 2),
                    min(0, (size[1] - im_to_paste.size[1]) // 2),
                ),
            )
            return im
        im = self._image_transpose_exif(
            Image.open(picture)
        )
        size = (config["width"], config["height"])
        scale_x = size[0] / im.size[0]
        scale_y = size[1] / im.size[1]
        if config["crop"]:
            scale = max(scale_x, scale_y)
        else:
            scale = min(scale_x, scale_y)
        size2 = tuple(int(round(value * scale)) for value in im.size)
        im = im.resize(size2, Image.ANTIALIAS)
        im = new_img(size, im)
        return im

    @staticmethod
    def _create_dir(file_path):
        dirname = os.path.dirname(file_path)
        if os.path.exists(dirname):
            return

        try:
            os.makedirs(dirname)
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    def resize(self, picture):
        for config in self.config['PICTURES_RESIZE_FORMATS']:
            directory, file_name = self.get_storage_path(picture)
            picture_path = os.path.join(directory, file_name)
            im = self._process_image_from_config(
                os.path.join(self.config['UPLOAD_DIRECTORY'], picture_path),
                config
            )
            destination = "{directory}/{width}x{height}x{crop}/{path}".format(
                directory=self.config['RESIZED_PICTURES_DIRECTORY'],
                width=config['width'],
                height=config['height'],
                crop=int(config['crop']),
                path=picture_path
            )
            self._create_dir(destination)
            im.save(destination, "JPEG", quality=95, optimize=True)
