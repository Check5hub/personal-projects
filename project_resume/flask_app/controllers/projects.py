from flask_app import app
from flask import Flask, render_template, redirect, request, session, flash
from flask_bcrypt import Bcrypt
from flask_app.models.project import Project
bcrypt = Bcrypt(app)

@app.route("/projects")
def projects():
    projects = Project.get_all()
    return render_template("projects.html", projects = projects)

@app.route("/edit_web_projects")
def edit_web_projects():
    return render_template("edit_web_projects.html")

@app.route("/edit_wood_projects")
def edit_wood_projects():
    return render_template("edit_wood_projects.html")

@app.route("/new_project")
def new_project():
    return render_template("new_project.html")

@app.route("/images")
def show_off():
    return render_template("p_images.html")

@app.route("/add_project", methods = ["POST"])
def add_project():
    valid = Project.valid_info(request.form)
    if valid:
        data = {
            "name" : request.form["name"],
            "description" : request.form["description"]
        }
        Project.add_project(data)
        return redirect("/projects")
    else:
        return redirect("/new_project")

@app.route("/edit/<int:id>")
def update_page(id):
    data = {
        "id" : id
    }
    project = Project.get_by_id(data)
    return render_template("edit_wood_projects.html", project = project)

@app.route("/update/<int:id>", methods = ["POST"])
def submit_update(id):
    valid = Project.valid_info(request.form)
    if valid:
        Project.update_project(request.form, id)
        return redirect("/projects")
    else:
        return redirect(f"/edit/{id}")

@app.route("/delete/<int:id>")
def delete(id):
    data = {
        "id" : id
    }
    Project.delete(data)
    return redirect("/projects")