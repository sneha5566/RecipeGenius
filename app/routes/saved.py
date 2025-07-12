from flask import Blueprint, render_template, redirect, request, url_for, session
from app.models import db, SavedRecipe
from datetime import datetime 

saved_bp = Blueprint('saved', __name__)

@saved_bp.route('/', methods=['GET'])
def view_saved():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    user_id = session['user_id']
    saved = SavedRecipe.query.filter_by(user_id=session['user_id']).all()
    return render_template('saved_recipes.html', saved=saved)

@saved_bp.route('/save', methods=['POST'])
def save_recipe():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    title = request.form['title']
    ingredients = request.form['ingredients']
    instructions = request.form['instructions']

    new_save = SavedRecipe(
        title=title,
        ingredients=ingredients,
        instructions=instructions,
        timestamp=datetime.utcnow(),
        user_id=session['user_id']
    )
    db.session.add(new_save)
    db.session.commit()
    return redirect(url_for('saved.view_saved'))

@saved_bp.route('/saved/delete/<int:recipe_id>')
def delete_saved(recipe_id):
    recipe = SavedRecipe.query.get_or_404(recipe_id)
    if recipe.user_id == session.get('user_id'):
        db.session.delete(recipe)
        db.session.commit()
    return redirect(url_for('saved.view_saved'))


@saved_bp.route('/save', methods=['POST'])
def add_to_saved():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    title = request.form.get('title')
    ingredients = request.form.get('ingredients')
    instructions = request.form.get('instructions')

    new_saved = SavedRecipe(
        user_id=session['user_id'],
        title=title,
        ingredients=ingredients,
        instructions=instructions,
        timestamp=datetime.utcnow()
    )

    db.session.add(new_saved)
    db.session.commit()

    return redirect(url_for('saved.view_saved'))  # Or wherever you want to go next

