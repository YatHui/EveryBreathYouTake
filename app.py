from datetime import datetime
from flask import Flask, render_template, request, url_for, redirect
from forms import CustomerEditForm, TransactionForm
from models import League, db, User, NewsAnnouncements, ChatMessage
from flask_migrate import Migrate, upgrade
from dash_app import init_dash,add_header,second_plot,third_plot

#Set up Flask
app = Flask(__name__)
app.config.from_object('config.ConfigDebug')

db.app = app
db.init_app(app)
migrate = Migrate(app, db)

# Initialize the Dash apps
init_dash(app)  
second_plot(app)
third_plot(app)

#Specify the routes
@app.route("/")
def indexPage():
    return render_template('index.html')

@app.route("/welcome")
def welcomePage():
    return render_template('welcome.html')

@app.route("/plots")
def plotsPage():
    return render_template('plots.html')

@app.route("/workflow")
def workflowPage():
    return render_template('workflow.html')

if __name__ == "__main__":
    with app.app_context():
        upgrade()
    app.run()





