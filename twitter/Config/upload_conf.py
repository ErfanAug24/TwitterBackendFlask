from flask_uploads import UploadSet, configure_uploads, IMAGES

photos = UploadSet("photos", IMAGES)


def init_app(app):
    configure_uploads(app, photos)
