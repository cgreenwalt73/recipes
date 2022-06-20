# import the function that will return an instance of a connection
from flask import flash, session
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)

# model the class after the user table from our database
class User:
    db = 'recipes_schema'

    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    # Now we use class methods to query our database
    @classmethod
    def add_user(cls, data):
        query="""
        INSERT INTO
        users ( first_name, last_name, email, password, created_at, updated_at)
        VALUES ( %(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW() )
        ;"""
        return connectToMySQL(cls.db).query_db(query, data)
    
    # class method to obtain a single user using email
    @classmethod
    def get_user_by_email(cls, email):
        data = { 'email' : email}
        query="""
        SELECT *
        FROM users
        WHERE email= %(email)s
        ;"""
        results= connectToMySQL(cls.db).query_db(query, data)
        return cls(results[0])

    # class method to obtain a single user using id
    @classmethod
    def get_user_by_id(cls, id):
        data= {'id' : id}
        query="""
        SELECT * 
        FROM users 
        WHERE id = %(id)s
        ;"""
        result= connectToMySQL(cls.db).query_db(query, data)
        return cls(result[0])

    @staticmethod
    def validate_user_registration(data):
        is_valid=True
        if len(data['first_name']) < 2:
            flash('First Name must be at least 2 characters')
            is_valid=False
        if len(data['last_name']) < 2:
            flash('Last Name must be at least 2 characters')
            is_valid=False
        if not EMAIL_REGEX.match(data['email']):
            flash('Email must have valid format')
            is_valid=False
        if data['cnfm_pass'] != data['password']:
            flash('Passwords do not match')
            is_valid=False
        return is_valid

    @staticmethod
    def validate_user_login(data):
        is_valid=True
        this_user = User.get_user_by_email(data['email'].lower())
        if not this_user:
            flash('Email not found')
            is_valid=False
        if len(this_user.password) < 1:
            flash('Password required')
            is_valid=False
        else:
            if bcrypt.check_password_hash(this_user.password, data['password']):
                session['user_id'] = this_user.id
                return True
            flash('Password incorrect')
            is_valid=False
        return is_valid