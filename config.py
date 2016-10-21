import os
CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

UPLOAD_FOLDER = 'forflask/static/database/'
ALLOWED_EXTENTIONS =set(['png','jpg','jpeg','bmp','gif'])
SQLALCHEMY_DATABASE_URL = 'sqlite:///' + os.path.join(os.path.abspath()+'/', 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(os.path.abspath()+'/', 'db_repository')
