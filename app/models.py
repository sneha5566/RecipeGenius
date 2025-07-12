from datetime import datetime

from app import db

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship to RecipeRequest
    recipe_requests = db.relationship('RecipeRequest', back_populates='user', lazy=True)

    def __repr__(self):
        return f"<User {self.username}>"

# Recipe request model
class RecipeRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ingredients = db.Column(db.Text, nullable=False)
    result = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Foreign key to User
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', back_populates='recipe_requests')

    def __repr__(self):
        return f"<RecipeRequest {self.ingredients[:20]}>"

# models.py

from datetime import datetime

class SavedRecipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(100), nullable=False)
    ingredients = db.Column(db.Text, nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)  # ✅ FIXED HERE

    def __repr__(self):
        return f"<SavedRecipe {self.title}>"



class MealPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recipe_name = db.Column(db.String(255), nullable=False)
    ingredients = db.Column(db.Text, nullable=True) 
    day_of_week = db.Column(db.String(20), nullable=False)



    user = db.relationship('User', backref='meal_plans')
class ShoppingItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    ingredient_name = db.Column(db.String(200), nullable=False)
    day_of_week = db.Column(db.String(20)) 
