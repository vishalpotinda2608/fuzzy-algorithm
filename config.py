import os
SECRECT_KEY=os.urandom(32)
basedir = os.path.abspath(os.path.dirname(__file__))
DEBUG=True
SQLALCHEMY_DATABASE_URI= 'your psycopg2 URI connection'
SQLALCHEMY_TRACK_MODIFICATIONS =True


