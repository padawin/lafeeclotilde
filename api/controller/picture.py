from .controller import Controller
from service.picture import PictureService, PictureSaveResult


class PictureController(Controller):
    def post(self, request):
        # checking if the file is present or not.
        if 'file' not in request.files:
            return self.format_response({'error': "Aucun fichier reçu"}), 400

        file = request.files['file']
        service = PictureService(self.config)
        res = service.save(file)
        body, status = self.create_response(res, {
            PictureSaveResult.OK: {},
            PictureSaveResult.INVALID_PICTURE_TYPE: (
                "Le fichier doit etre une image JPEG", 400
            )
        })
        return self.format_response(body), status
