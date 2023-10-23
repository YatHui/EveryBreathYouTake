from datetime import datetime
from flask import Flask, render_template, request, url_for, redirect
from forms import CustomerEditForm, UserEditForm, EmailEditForm, TransactionForm, DepositForm, WithdrawalForm
from models import League, db,user_manager,Standings, User, Goalie, Team, CurrentRound, Skater,TeamSkater,TeamGoalie,SkaterStats,GoalieStats,TradeLog,ScoringRules,NewsAnnouncements,Notifications,ChatMessage,UserLog
from flask_migrate import Migrate, upgrade
from flask_user import login_required, roles_required, roles_accepted, current_user
from flask_login import login_required, current_user


app = Flask(__name__)
app.config.from_object('config.ConfigDebug')

db.app = app
db.init_app(app)
migrate = Migrate(app,db)
user_manager.app = app
user_manager.init_app(app,db,User)



@app.route("/")
def indexPage():
    return render_template('index.html')



if __name__  == "__main__":
    with app.app_context():
        upgrade()
    app.run()