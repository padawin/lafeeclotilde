import errno
import functools
import json
import os
from enum import Enum, auto
from PIL import Image, ExifTags
import werkzeug

from model.model import Model
from model.picture import PictureModel

from common.service import picture


class PictureSaveResult(Enum):
    OK = auto()
    INVALID_PICTURE_TYPE = auto()


class PictureService(picture.PictureService):
    _interesting_exif = {
        'DateTime', 'DateTimeDigitized', 'DateTimeOriginal',
        'DigitalZoomRatio', 'ExifImageHeight', 'ExifImageWidth',
        'ExifInteroperabilityOffset', 'ExifOffset', 'ExifVersion',
        'ExposureBiasValue', 'ExposureMode', 'ExposureProgram', 'ExposureTime',
        'FNumber', 'FileSource', 'Flash', 'FlashPixVersion', 'FocalLength',
        'FocalLengthIn35mmFilm', 'GPSInfo', 'GainControl', 'ISOSpeedRatings',
        'LightSource', 'Make',
    }

    def __init__(self, config):
        self.config = config

    def save(self, file):
        if file.mimetype != 'image/jpeg':
            return PictureSaveResult.INVALID_PICTURE_TYPE, None
        file_name = werkzeug.secure_filename(file.filename)
        picture = {"file_name": file_name}
        picture["id_picture"] = picture_id = PictureModel.insert(picture)
        directory, file_name = self.get_storage_path(picture)
        relative_file_path = os.path.join(directory, file_name)
        file_path = self.save_file(file, relative_file_path)
        picture['exif'] = json.dumps(self._get_file_exif(file_path))
        PictureModel.update(picture, ['id_picture = %s', [picture_id]])
        self.resize(relative_file_path)
        Model.commit()
        return PictureSaveResult.OK, None

    @classmethod
    def _get_file_exif(cls, file_path):
        img = Image.open(file_path)
        exifs = img._getexif()
        if not exifs:
            exifs = dict()
        exif_data = {
            ExifTags.TAGS[k]: str(v)
            for k, v in exifs.items()
            if k in ExifTags.TAGS and ExifTags.TAGS[k] in cls._interesting_exif
        }
        return exif_data

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

    def save_file(self, file, relative_file_path):
        file_path = os.path.join(
            self.config['UPLOAD_DIRECTORY'], relative_file_path
        )
        self._create_dir(file_path)
        # save the file
        file.save(file_path)
        return file_path

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

    def resize(self, picture_path):
        for config in self.config['PICTURES_RESIZE_FORMATS']:
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

    def get_all(self, offset, limit):
        pictures = PictureModel.loadAll(
            order_fields={'id_picture': 'desc'}, limit=limit, offset=offset
        )
        total_count = PictureModel.count()
        for pic in pictures:
            pic['date_created'] = (
                pic['date_created'].isoformat()
                if pic['date_created'] else
                ''
            )
        return pictures, total_count
