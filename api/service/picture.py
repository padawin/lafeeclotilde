import hashlib
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
        filename = werkzeug.secure_filename(file.filename)
        # generate image sha1
        file_hash = hashlib.sha1(
            f"{id}-{filename}".encode('ascii')
        ).hexdigest()
        # create the directory structure
        n = 5
        dir_structure = [file_hash[i:i+n] for i in range(0, len(file_hash), n)]
        directory = os.path.join(
            self.config['UPLOAD_DIRECTORY'], *dir_structure
        )
        if not os.path.exists(directory):
            os.makedirs(directory)
        # save the file
        file_path = os.path.join(directory, f"{file_hash}-{id}-{filename}")
        file.save(file_path)
        return file_hash, file_path

    def get_all(self):
        pictures = PictureModel.loadAll()
        for picture in pictures:
            picture['date_created'] = (
                picture['date_created'].isoformat()
                if picture['date_created'] else
                ''
            )
        return pictures
