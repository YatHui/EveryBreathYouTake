from secret_info import master_password, url, url2
from sqlalchemy import create_engine


class ConfigDebug():
    SQLALCHEMY_DATABASE_URI = url2    # Postgres database
    SECRET_KEY = master_password
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    

    # DATABASE_URL = url # Postgres database
    # engine = create_engine(DATABASE_URL)

