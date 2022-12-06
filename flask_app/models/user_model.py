from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash
import re
from flask_bcrypt import Bcrypt
from flask_app import app

bcrypt = Bcrypt(app)

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data["last_name"]
        self.username = data['username']
        self.email = data["email"]
        self.password = data['password']
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(DATABASE).query_db(query)

        all_users = []
        for user in results:
            all_users.append(user)

        return all_users

    @classmethod
    def get_user_by_id(cls, data):
        query = 'SELECT * FROM users '
        query += 'WHERE id = %(user_id)s;'
        result = connectToMySQL(DATABASE).query_db(query, data)
        return cls(result[0])

    @classmethod
    def get_one_email(cls, data):
        query = "SELECT * FROM users "
        query += "WHERE email = %(email)s"

        result = connectToMySQL(DATABASE).query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def create_login(cls, data):
        query = "INSERT INTO users (first_name, last_name, username, email, password) "
        query += "VALUES (%(first_name)s, %(last_name)s, %(username)s,%(email)s, %(password)s)"

        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def update_user(cls, data):
        query = 'UPDATE users '
        query += 'SET first_name = %(first_name)s, last_name = %(last_name)s, username = %(username)s, email = %(email)s '
        query += 'WHERE id = %(id)s'
        return connectToMySQL(DATABASE).query_db(query, data)

    @staticmethod
    def validate_email(email):
        is_valid = True

        if User.get_one_email(email):
            flash("Email address is already in use!", 'email_error')
            is_valid = False
        elif not EMAIL_REGEX.match(email['email']):
            flash("Invalid email address!", 'email_error')
            is_valid = False
        return is_valid
