from model.model import Model


class PictureModel(Model):
    fields = ('id_picture', 'file_name', 'hash', 'exif', 'date_created')
