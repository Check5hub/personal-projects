from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

db = "resume_schema"

class Project:
    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.description = data["description"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        
    @staticmethod
    def valid_info(project_info):
        is_valid = True
        if len(project_info["name"]) < 3:
            flash("You forgot to name your project.")
            is_valid = False
        if len(project_info["description"]) < 8:
            flash("Say a bit more about your project.")
            is_valid = False
        return is_valid

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM projects;"
        results = connectToMySQL(db).query_db(query)
        projects = []
        for project in results:
            projects.append(cls(project))
        return projects

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM projects WHERE id = %(id)s;"
        result = connectToMySQL(db).query_db(query, data)
        return cls(result[0])

    @classmethod
    def add_project(cls, data):
        query = "INSERT INTO projects (name, description) VALUES (%(name)s, %(description)s);"
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def update_project(cls, data, id):
        query = f"UPDATE projects SET name = %(name)s, description = %(description)s WHERE id = {id};"
        result = connectToMySQL(db).query_db(query, data)
        return result

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM projects WHERE id = %(id)s;"
        return connectToMySQL(db).query_db(query, data)