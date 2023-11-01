from datetime import datetime
from flask import Flask, render_template, request, url_for, redirect,jsonify
from forms import CustomerEditForm, TransactionForm
from models import League, db, User, NewsAnnouncements, ChatMessage
from flask_migrate import Migrate, upgrade
from dash_app import init_dash,add_header,second_plot,third_plot,fourth_plot
from secret_info import api_key
import openai

#Set up Flask
app = Flask(__name__)
app.config.from_object('config.ConfigDebug')
openai.api_key = api_key

db.app = app
db.init_app(app)
migrate = Migrate(app, db)

# Initialize the Dash apps
init_dash(app)  
second_plot(app)
third_plot(app)
fourth_plot(app)

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

@app.route("/predictions")
def predictionsPage():
    return render_template('predictions.html')

@app.route("/workflow")
def workflowPage():
    return render_template('workflow.html')

@app.route("/tech", methods=['GET', 'POST'])
def techPage():
    return render_template('tech.html')


@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    system_message = request.json.get('system', "Hello, I'm ready to chat about pollution and health effects.")
    if not user_message:
        return jsonify({'error': 'User message is required'}), 400

    # Using OpenAI API to get a response
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": system_message
            },
            {
                "role": "user",
                "content": user_message
            }
        ],
        temperature=1,
        max_tokens=180,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    gpt_response = response.choices[0].message.content.strip()
    return jsonify({'response': gpt_response})


if __name__ == "__main__":
    with app.app_context():
        upgrade()
    app.run()









