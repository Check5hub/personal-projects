from flask import flash
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
import re

db = "resume_schema"
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @staticmethod
    def valid_register(user_info):
        is_valid = True
        query = "SELECT * FROM admin WHERE email = %(email)s;"
        result = connectToMySQL(db).query_db(query, user_info)
        if len(result) >= 1:
            flash("Email already in use", "register")
            is_valid = False
        if len(user_info["first_name"]) < 3:
            flash("First name required.", "register")
            is_valid = False
        if len(user_info["last_name"]) < 3:
            flash("Last name required.", "register")
            is_valid = False
        if not EMAIL_REGEX.match(user_info["email"]):
            flash("Invalid email address.", "register")
            is_valid = False
        if len(user_info["password"]) < 8:
            flash("Password must be at least 8 characters.", "register")
            is_valid = False
        return is_valid

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM admin WHERE email = %(email)s"
        results = connectToMySQL(db).query_db(query, data)
        if len(results) < 1:
            return False
        return (cls(results[0]))

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM admin WHERE id = %(id)s"
        results = connectToMySQL(db).query_db(query, data)
        return (cls(results[0]))

    @classmethod
    def create(cls, data):
        query = "INSERT INTO admin (first_name, last_name, email, password ) VALUES ( %(first_name)s, %(last_name)s, %(email)s, %(pw_hash)s);"
        return connectToMySQL(db).query_db(query, data)