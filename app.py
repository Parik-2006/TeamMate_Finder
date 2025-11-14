
from flask import Flask, render_template, session, redirect, url_for, request
from flask_session import Session
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)

# --- Configuration (replace with your values) ---
app.secret_key =SECRET_KEY
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# OAuth setup using Authlib
oauth = OAuth(app)
oauth.register(
    name="google",
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    access_token_url="https://oauth2.googleapis.com/token",
    authorize_url="https://accounts.google.com/o/oauth2/v2/auth",
    api_base_url="https://www.googleapis.com/oauth2/v1/",
    client_kwargs={"scope": "openid email profile"},
)


@app.route("/")
def index():
    user = session.get("user")
    return render_template("index.html", user=user)


@app.route("/login")
def login():
    # Show a login page with a Google sign-in button
    return render_template("login.html")


@app.route("/login/google")
def login_google():
    # Start OAuth redirect flow
    redirect_uri = url_for("authorize", _external=True)
    return oauth.google.authorize_redirect(redirect_uri)


@app.route("/authorize")
def authorize():
    # Handle callback from Google
    token = oauth.google.authorize_access_token()
    if not token:
        return redirect(url_for("index"))

    resp = oauth.google.get("userinfo")
    user_info = resp.json()

    # Save the user info in session
    session["user"] = {
        "name": user_info.get("name"),
        "email": user_info.get("email"),
        "picture": user_info.get("picture"),
    }

    user = session.get("user")
    return render_template("index.html", user=user)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)

