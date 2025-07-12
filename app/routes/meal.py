from flask import Blueprint, render_template, session, redirect, url_for

meal_bp = Blueprint('meal', __name__)

@meal_bp.route('/meal-planner')
def meal_planner():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    return render_template('meal_planner.html')

"""@meal_bp.route('/shopping-list')
def shopping_list():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    return render_template('shopping_list.html')"""
