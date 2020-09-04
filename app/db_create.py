#!flask/bin/python
from migrate.versioning import api
from app.config import Config#SQLALCHEMY_DATABASE_URI
#from app.config import SQLALCHEMY_MIGRATE_REPO
from app import db
import os.path


def main():
    db.create_all()
    SQLALCHEMY_MIGRATE_REPO = Config.SQLALCHEMY_MIGRATE_REPO
    SQLALCHEMY_DATABASE_URI = Config.SQLALCHEMY_DATABASE_URI
    if not os.path.exists(SQLALCHEMY_MIGRATE_REPO):
        api.create(SQLALCHEMY_MIGRATE_REPO, 'database repository')
        api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
    else:
        api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, api.version(SQLALCHEMY_MIGRATE_REPO))

main()