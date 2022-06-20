from flask import flash, session
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL

class Recipe:
    db = 'recipes_schema'

    def __init__( self , data ):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_made = data['date_made']
        self.under30min = data['under30min']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
    
    @classmethod
    def get_all_recipes(cls):
        query = """
        SELECT * 
        FROM recipes
        ;"""
        results = connectToMySQL(cls.db).query_db(query)
        recipes = []
        for recipe in results:
            recipes.append( cls(recipe) )
        return recipes

    # Now we use class methods to query our database
    @classmethod
    def add_recipe(cls, data):
        query="""
        INSERT INTO
        recipes ( name, description, instructions, date_made, under30min, created_at, updated_at, user_id)
        VALUES ( %(name)s, %(description)s, %(instructions)s, %(date_made)s, %(under30min)s, NOW(), NOW(), %(user_id)s )
        ;"""
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def get_recipe_by_id(cls, id):
        data= {'id' : id}
        query="""
        SELECT * 
        FROM recipes
        WHERE id = %(id)s
        ;"""
        result= connectToMySQL(cls.db).query_db(query, data)
        return cls(result[0])

    @classmethod
    def edit_recipe(cls, data):
        query="""
        UPDATE recipes
        SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, date_made = %(date_made)s, under30min = %(under30min)s, updated_at = NOW()
        WHERE id = %(id)s
        ;"""
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def delete_recipe(cls, id):
        data= {'id' : id}
        query="""
        DELETE FROM recipes 
        WHERE recipes.id= %(id)s
        ;"""
        return connectToMySQL(cls.db).query_db(query, data)

    @staticmethod
    def validate_recipe(recipe):
        is_valid=True
        if len(recipe['name']) < 3:
            flash("Name must be at least 3 characters")
            is_valid=False
        if len(recipe['description']) < 3:
            flash("Description must be at least 3 characters")
            is_valid=False
        if len(recipe['instructions']) < 3:
            flash("Instructions must be at least 3 characters")
            is_valid=False
        if not recipe['date_made']:
            flash("You must select a date")
            is_valid=False
        if 'under30min' not in recipe:
            flash("You must select an option")
            is_valid=False
        return is_valid