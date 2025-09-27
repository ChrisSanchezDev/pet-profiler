from flask import Flask, redirect, session, render_template
from authlib.integrations.flask_client import OAuth
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()
from dotenv import load_dotenv
load_dotenv()  # load .env
import os

from flask import Flask, redirect, session
from authlib.integrations.flask_client import OAuth

# --- Flask app setup ---
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
app.secret_key = os.getenv("SECRET_KEY", "some_random_secret_string")

# --- Auth0 setup ---
oauth = OAuth(app)
auth0 = oauth.register(
    'auth0',
    client_id="QLuukUUxo4jA3QZHiOnDAlRJU7qJLAMU",
    client_secret="X22pMRLhdJr-ET7INjfYqzQYZcZCtTSJB-tpvm40F_L7Q3YLoGf1C0QkH2h9DgmZ",
    client_kwargs={'scope': 'openid profile email'},
    server_metadata_url=f'https://{os.getenv("AUTH0_DOMAIN")}/.well-known/openid-configuration'
)

# --- Routes ---

# Auto-redirect home to login
@app.route("/")
def home():
        return '<a href="/login">Login with Auth0</a>'

@app.route("/login")
def login():
    return auth0.authorize_redirect(redirect_uri=os.getenv('AUTH0_CALLBACK_URL'))

# Login route
@app.route("/login")
def login():
    return auth0.authorize_redirect(redirect_uri="http://127.0.0.1:5000/callback")

# Callback route
@app.route("/callback")
def callback():
    token = auth0.authorize_access_token()
    resp = auth0.get('userinfo')
    user_info = resp.json()
    session['user'] = user_info
    return redirect("/dashboard")

# Dashboard route
@app.route("/dashboard")
def dashboard():
    if 'user' not in session:
        return redirect("/login")
    return f"Hello {session['user']['name']}! Welcome to your dashboard."

# Logout route
@app.route("/logout")
def logout():
    session.clear()
    return redirect(
        f'https://{os.getenv("AUTH0_DOMAIN")}/v2/logout?returnTo=http://localhost:5000'
    )

        'https://dev-77sq72oygyojf28x.us.auth0.com/v2/logout?returnTo=http://127.0.0.1:5000'
    )

# --- Run app ---
if __name__ == "__main__":
    app.run(debug=True)
