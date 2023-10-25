from datetime import datetime
from flask import Flask, render_template, request, url_for, redirect
from forms import CustomerEditForm,TransactionForm
from models import League, db, User,NewsAnnouncements,ChatMessage
from flask_migrate import Migrate, upgrade
# from flask_user import login_required, roles_required, roles_accepted, current_user
# from flask_login import login_required, current_user
from datetime import datetime
from flask import Flask, render_template, request, url_for, redirect
from forms import CustomerEditForm, TransactionForm
from models import League, db, User, NewsAnnouncements, ChatMessage
from flask_migrate import Migrate, upgrade
import dash
import dash_core_components as dcc
import dash_html_components as html

app = Flask(__name__)
app.config.from_object('config.ConfigDebug')

db.app = app
db.init_app(app)
migrate = Migrate(app,db)


#DASH
dash_app = dash.Dash(
    __name__,
    server=app,
    routes_pathname_prefix='/dash/'
)

dash_app.layout = html.Div([
    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': 'Montréal'},
            ],
            'layout': {
                'title': 'Dash Data Visualization'
            }
        }
    )
])

#Dash end
@app.route("/")
def indexPage():
    return render_template('index.html')

if __name__  == "__main__":
    with app.app_context():
        upgrade()
    app.run()




