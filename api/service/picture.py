import errno
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

    def get_all(self, offset, limit):
        pictures = PictureModel.loadAll(limit=limit, offset=offset)
        total_count = PictureModel.count()
        for pic in pictures:
            pic['date_created'] = (
                pic['date_created'].isoformat()
                if pic['date_created'] else
                ''
            )
        return pictures, total_count
