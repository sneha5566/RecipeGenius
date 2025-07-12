from flask import Blueprint, render_template, request, redirect, url_for, session
from app.models import db, RecipeRequest
from app.utils.ai_utils import generate_recipe
from datetime import datetime

bp = Blueprint('recipe', __name__)

@bp.route('/recipe', methods=['GET', 'POST'])
def recipe_suggest():
    if request.method == 'POST':
        ingredients = request.form['ingredients']
        time = request.form.get('time', '')
        difficulty = request.form.get('difficulty', '')
        cuisine = request.form.get('cuisine', '')

        # Build prompt
        prompt_parts = [f"Write a {difficulty} {cuisine} recipe"]
        if time:
            prompt_parts.append(f"that takes {time}")
        prompt_parts.append(f"using the following ingredients: {ingredients}.")
        prompt = " ".join(part for part in prompt_parts if part.strip())

        # Call AI
        recipe_data = generate_recipe(prompt)

        # Save in DB
        recipe_id = None
        if 'user_id' in session:
            new_entry = RecipeRequest(
                ingredients=ingredients,
                result=recipe_data['instructions'],
                user_id=session['user_id'],
                timestamp=datetime.utcnow()
            )
            db.session.add(new_entry)
            db.session.commit()
            recipe_id = new_entry.id

        # Render full recipe immediately
        return render_template("recipe_detail.html", recipe=recipe_data, recipe_id=recipe_id)

    return render_template("recipe.html")


@bp.route('/history')
def view_history():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login'))

    # 🕘 Get all user recipe requests
    requests = RecipeRequest.query.filter_by(user_id=user_id).order_by(RecipeRequest.timestamp.desc()).all()
    return render_template("history.html", requests=requests)


@bp.route('/recipe/<int:recipe_id>')
def recipe_detail(recipe_id):
    recipe = RecipeRequest.query.get_or_404(recipe_id)

    # 📦 Format saved entry for display
    recipe_data = {
        'id': recipe.id,
        'title': f"Recipe from {recipe.ingredients}",
        'ingredients': recipe.ingredients.split(','),  # assumes comma-separated
        'instructions': recipe.result,
        'cook_time': 'N/A',
        'nutrition_text': 'Estimate not available'
    }

    return render_template("recipe_detail.html", recipe=recipe_data)

@bp.route('/substitutes', methods=['POST'])
def view_substitutes():
    # Placeholder logic (you can improve it later)
    return "Substitutes feature coming soon!"

