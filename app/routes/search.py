# app/routes/search.py

from flask import Blueprint, render_template, request, session, redirect, url_for
from app.utils.ai_utils import generate_recipe  # Optional: use for AI search later

search_bp = Blueprint('search', __name__)

@search_bp.route('/search', methods=['GET', 'POST'])
def search():
    results = []
    if request.method == 'POST':
        ingredients = request.form.get('ingredients')
        time = request.form.get('time')
        difficulty = request.form.get('difficulty')

        # For now, just show a fake result or call `generate_recipe`
        if ingredients:
            results = [
                {
                    "title": "Tomato Egg Stir Fry",
                    "summary": f"A simple dish using: {ingredients}",
                    "time": time or "15 mins",
                    "difficulty": difficulty or "Easy"
                }
            ]
    return render_template('search.html', results=results)
