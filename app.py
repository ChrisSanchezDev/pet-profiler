from flask import Flask, redirect, session, render_template
from authlib.integrations.flask_client import OAuth
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)
app.secret_key = 'RANDOM_SECRET_KEY'  # Replace with a long random string

# Auth0 setup
oauth = OAuth(app)
auth0 = oauth.register(
    'auth0',
    client_id=os.getenv('AUTH0_CLIENT_ID'),
    client_secret=os.getenv('AUTH0_CLIENT_SECRET'),
    api_base_url=f'https://{os.getenv("AUTH0_DOMAIN")}',
    access_token_url=f'https://{os.getenv("AUTH0_DOMAIN")}/oauth/token',
    authorize_url=f'https://{os.getenv("AUTH0_DOMAIN")}/authorize',
    client_kwargs={'scope': 'openid profile email'}
)

# Routes
@app.route("/")
def home():
    return "Hello World!"

@app.route("/login")
def login():
    return auth0.authorize_redirect(redirect_uri=os.getenv('AUTH0_CALLBACK_URL'))

@app.route("/callback")
def callback():
    token = auth0.authorize_access_token()
    resp = auth0.get('userinfo')
    user_info = resp.json()
    session['user'] = user_info
    return redirect("/dashboard")

@app.route("/dashboard")
def dashboard():
    if 'user' not in session:
        return redirect("/login")
    return f"Hello {session['user']['name']}! Welcome to your dashboard."

@app.route("/logout")
def logout():
    session.clear()
    return redirect(
        f'https://{os.getenv("AUTH0_DOMAIN")}/v2/logout?returnTo=http://localhost:5000'
    )

if __name__ == "__main__":
    app.run(debug=True)
