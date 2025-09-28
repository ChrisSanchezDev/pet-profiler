from flask import Flask, redirect, url_for, session
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)
app.secret_key = "write1"  # replace with a real secret in production

# Auth0 configuration
AUTH0_DOMAIN = "dev-77sq72oygyojf28x.us.auth0.com"
AUTH0_CLIENT_ID = "QLuukUUxo4jA3QZHiOnDAlRJU7qJLAMU"
AUTH0_CLIENT_SECRET = "X22pMRLhdJr-ET7INjfYqzQYZcZCtTSJB-tpvm40F_L7Q3YLoGf1C0QkH2h9DgmZ"
AUTH0_CALLBACK_URL = "http://127.0.0.1:5000/callback"
AUTH0_LOGOUT_URL = "http://127.0.0.1:5000"

oauth = OAuth(app)
auth0 = oauth.register(
    "auth0",
    client_id=AUTH0_CLIENT_ID,
    client_secret=AUTH0_CLIENT_SECRET,
    api_base_url=f"https://{AUTH0_DOMAIN}",
    access_token_url=f"https://{AUTH0_DOMAIN}/oauth/token",
    authorize_url=f"https://{AUTH0_DOMAIN}/authorize",
    client_kwargs={
        "scope": "openid profile email",
    },
)

@app.route("/")
def home():
    return '<a href="/login">Log In</a>'

@app.route("/login")
def login():
    return auth0.authorize_redirect(redirect_uri=AUTH0_CALLBACK_URL)

@app.route("/callback")
def callback():
    token = auth0.authorize_access_token()
    # <--- IMPORTANT: use the FULL URL here
    resp = auth0.get('https://dev-77sq72oygyojf28x.us.auth0.com/userinfo')
    userinfo = resp.json()
    session["user"] = userinfo
    return f"Hello {userinfo['name']}!"

@app.route("/logout")
def logout():
    session.clear()
    return redirect(f"{AUTH0_LOGOUT_URL}")

if __name__ == "__main__":
    app.run(debug=True)
