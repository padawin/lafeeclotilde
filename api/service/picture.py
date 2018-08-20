import hashlib
import os
from enum import Enum, auto
import werkzeug


class PictureSaveResult(Enum):
    OK = auto()
    INVALID_PICTURE_TYPE = auto()


class PictureService:
    def __init__(self, config):
        self.config = config

    def save(self, file):
        if file.mimetype != 'image/jpeg':
            return PictureSaveResult.INVALID_PICTURE_TYPE, None
        self.save_file(file)
        return PictureSaveResult.OK, None

    def save_file(self, file):
        filename = werkzeug.secure_filename(file.filename)
        # generate image sha1
        file_hash = hashlib.sha1(
            filename.encode('ascii')
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
        file.save(os.path.join(
            directory,
            f"{file_hash}-{filename}"
        ))
