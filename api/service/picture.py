import os
import json
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
        picture_id = PictureModel.insert({
            'file_name': file.filename,
        })
        file_hash, file_path = self.save_file(file, picture_id)
        PictureModel.update(
            {
                'hash': file_hash,
                'exif': json.dumps(self._get_file_exif(file_path))
            },
            ['id_picture = %s', [picture_id]]
        )
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

    def save_file(self, file, id):
        file_name = werkzeug.secure_filename(file.filename)
        picture = {"id_picture": id, "file_name": file_name}
        directory, file_name = self.get_storage_path(picture)
        directory = os.path.join(self.config['UPLOAD_DIRECTORY'], directory)
        # create the directory structure
        if not os.path.exists(directory):
            os.makedirs(directory)
        # save the file
        file_path = os.path.join(directory, file_name)
        file.save(file_path)
        return picture['hash'], file_path

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
