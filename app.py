from datetime import datetime
from flask import Flask, render_template, request, url_for, redirect
from forms import CustomerEditForm,TransactionForm
from models import League, db, User,NewsAnnouncements,ChatMessage
from flask_migrate import Migrate, upgrade
# from flask_user import login_required, roles_required, roles_accepted, current_user
# from flask_login import login_required, current_user


app = Flask(__name__)
app.config.from_object('config.ConfigDebug')

db.app = app
db.init_app(app)
migrate = Migrate(app,db)

@app.route("/")
def indexPage():
    return render_template('index.html')

if __name__  == "__main__":
    with app.app_context():
        upgrade()
    app.run()




