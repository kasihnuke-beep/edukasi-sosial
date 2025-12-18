from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = "ai-lingkungan"

UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

users = {}

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if users.get(request.form["username"]) == request.form["password"]:
            session["user"] = request.form["username"]
            return redirect("/dashboard")
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        users[request.form["username"]] = request.form["password"]
        return redirect("/")
    return render_template("register.html")

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "user" not in session:
        return redirect("/")
    
    if request.method == "POST":
        photo = request.files["photo"]
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], photo.filename)
        photo.save(filepath)

        # Dummy AI Classification
        result = "Lingkungan Bersih 🌊" if "bersih" in photo.filename.lower() else "Lingkungan Tercemar ⚠️"

        return render_template("result.html", img=photo.filename, result=result)

    return render_template("dashboard.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
