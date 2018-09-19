import hashlib
import os


class PictureService:
    @staticmethod
    def get_storage_path(picture):
        file_hash = hashlib.sha1(
            "{id}-{file_name}".format(
                id=picture["id_picture"],
                file_name=picture["file_name"]
            ).encode('ascii')
        ).hexdigest()

        n = 5
        dir_structure = [file_hash[i:i+n] for i in range(0, len(file_hash), n)]
        directory = os.path.join(*dir_structure)
        file_name = "{file_hash}-{id}-{file_name}".format(
            file_hash=file_hash,
            id=picture["id_picture"],
            file_name=picture["file_name"]
        )
        return directory, file_name, file_hash
