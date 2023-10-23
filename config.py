from secret_info import master_password, url

class ConfigDebug():
   SQLALCHEMY_DATABASE_URI = url    # Postgres database
   SECRET_KEY = master_password


   # Flask-User settingsa
   USER_APP_NAME = "Flask-User Basic App"      # Shown in and email templates and page footers
   USER_ENABLE_EMAIL = True        # Enable email aution
   USER_ENABLE_USERNAME = False    # Disable username authentication
   USER_EMAIL_SENDER_NAME = USER_APP_NAME
   USER_EMAIL_SENDER_EMAIL = "noreply@example.com" 
