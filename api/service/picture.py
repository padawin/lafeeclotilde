from enum import Enum, auto


class PictureSaveResult(Enum):
    OK = auto()
    INVALID_PICTURE_TYPE = auto()


class PictureService:
    def save(self, file):
        if file.mimetype != 'image/jpeg':
            return PictureSaveResult.INVALID_PICTURE_TYPE, None
        return PictureSaveResult.OK, None
