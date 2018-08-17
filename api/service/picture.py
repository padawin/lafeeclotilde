from enum import Enum, auto


class PictureSaveResult(Enum):
    OK = auto()


class PictureService:
    def save(self, file):
        return PictureSaveResult.OK
