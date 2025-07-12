# routes/nutrition.py
from flask import Blueprint, render_template, request
from app.utils.llm_utils import generate_nutrition

nutrition_bp = Blueprint('nutrition', __name__)

@nutrition_bp.route('/nutrition', methods=['GET', 'POST'])
def nutrition_page():
    nutrition_info = None
    if request.method == 'POST':
        dish = request.form['dish']
        nutrition_info = generate_nutrition(dish)
    return render_template('nutrition.html', nutrition_info=nutrition_info)
