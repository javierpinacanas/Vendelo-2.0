from flask import Flask, render_template, request, redirect, url_for, session
import os
import json

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secure key for sessions

# File-based "database"
DATA_FILE = "data.json"

# Helper function to load/save data
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {"users": {}, "listings": {}}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

# Home page - Browse listings
@app.route("/")
def index():
    data = load_data()
    listings = data["listings"]
    return render_template("index.html", listings=listings)

# Login page
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        data = load_data()
        if username in data["users"] and data["users"][username] == password:
            session["username"] = username
            return redirect(url_for("index"))
        return "Invalid credentials"
    return render_template("login.html")

# Signup page
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        data = load_data()
        if username not in data["users"]:
            data["users"][username] = password
            save_data(data)
            session["username"] = username
            return redirect(url_for("index"))
        return "Username taken"
    return render_template("signup.html")

# Create listing
@app.route("/create", methods=["GET", "POST"])
def create_listing():
    if "username" not in session:
        return redirect(url_for("login"))
    if request.method == "POST":
        title = request.form["title"]
        desc = request.form["description"]
        price = request.form["price"]
        data = load_data()
        listing_id = str(len(data["listings"]) + 1)
        data["listings"][listing_id] = {
            "title": title,
            "description": desc,
            "price": price,
            "seller": session["username"]
        }
        save_data(data)
        return redirect(url_for("index"))
    return render_template("create_listing.html")

# Logout
@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
