from flask_app import app
from flask import Flask, render_template, redirect, request, session, flash
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route("/")
def index():
    return render_template("home.html")

@app.route("/skills")
def skills():
    return render_template("skills.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/admin")
def admin():
    return render_template("admin.html")

@app.route("/edit_skills")
def edit_skills():
    return render_template("edit_skills.html")

@app.route("/login", methods = ["POST"])
def login():
    user = User.get_by_email(request.form)
    if not user:
        flash("Invalid email","login")
        print("invalid email")
        return redirect("/admin")
    if not bcrypt.check_password_hash(user.password, request.form["password"]):
        flash("Invalid password","login")
        return redirect("/admin")
    session["admin_email"] = "admin.email"
    print("you made it past login")
    return redirect('/login_success')

@app.route("/login_success")
def admin_dashboard():
    if "admin_email" not in session:
        return redirect("/logout")
    return render_template("edit_dashboard.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/register", methods = ["POST"])
def register():
    data = {
        "first_name" : request.form["first_name"],
        "last_name" : request.form["last_name"],
        "email" : request.form["email"],
        "password" : request.form["password"],
    }
    valid = User.valid_register(data)
    if valid:
        pw_hash = bcrypt.generate_password_hash(request.form["password"])
        data["pw_hash"] = pw_hash
        user = User.create(data)
        session["user_id"] = user
        return redirect("/")
    return redirect("/")