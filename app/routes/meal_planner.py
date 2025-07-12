from flask import Blueprint, render_template, request, redirect, url_for, session
from app.models import db, MealPlan, RecipeRequest, ShoppingItem
from datetime import datetime
import csv
import io

planner_bp = Blueprint('meal_planner', __name__)

@planner_bp.route('/meal-planner', methods=['GET', 'POST'])
def meal_planner():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    user_id = session['user_id']

    if request.method == 'POST':
        recipe_name = request.form['recipe_name']
        day = request.form['day']
        ingredients_text = request.form.get('ingredients', '').strip()

        # ✅ Fallback to latest recipe if ingredients not entered
        if not ingredients_text:
            latest_recipe = RecipeRequest.query.filter_by(user_id=user_id).order_by(RecipeRequest.timestamp.desc()).first()
            if not latest_recipe:
                return "❗ No recent recipe found. Please enter ingredients or generate a recipe.", 400
            ingredients_text = latest_recipe.ingredients

        # ✅ Split ingredients
        ingredients_list = ingredients_text.split(',') if ',' in ingredients_text else ingredients_text.split('\n')

        # ✅ Create MealPlan
        new_plan = MealPlan(
            user_id=user_id,
            recipe_name=recipe_name,
            day_of_week=day,
            ingredients=ingredients_text
        )
        db.session.add(new_plan)

        # ✅ Add ingredients to shopping list
        for ing in ingredients_list:
            clean_ing = ing.strip()
            if clean_ing:
                db.session.add(ShoppingItem(
                    user_id=user_id,
                    ingredient_name=clean_ing,
                    day_of_week=day
                ))

        db.session.commit()
        return redirect(url_for('meal_planner.meal_planner'))

    plans = MealPlan.query.filter_by(user_id=user_id).all()
    return render_template('meal_planner.html', plans=plans)

# ✅ Edit Meal Plan
@planner_bp.route('/meal-planner/edit/<int:plan_id>', methods=['GET', 'POST'])
def edit_plan(plan_id):
    plan = MealPlan.query.get_or_404(plan_id)

    if request.method == 'POST':
        plan.recipe_name = request.form['recipe_name']
        plan.day_of_week = request.form['day']
        plan.ingredients = request.form.get('ingredients', '')
        db.session.commit()
        return redirect(url_for('meal_planner.meal_planner'))

    return render_template('edit_plan.html', plan=plan)



# Delete Meal Plan
@planner_bp.route('/meal-planner/delete/<int:plan_id>')
def delete_plan(plan_id):
    plan = MealPlan.query.get_or_404(plan_id)
    db.session.delete(plan)
    db.session.commit()
    return redirect(url_for('meal_planner.meal_planner'))


# Generate Shopping List
"""@planner_bp.route('/shopping-list')
def shopping_list():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    plans = MealPlan.query.filter_by(user_id=user_id).all()

    ingredient_list = []

    for plan in plans:
        if plan.ingredients:
            # Split by comma and strip whitespace
            ingredient_list += [item.strip().lower() for item in plan.ingredients.split(',')]

    # Remove duplicates and sort
    unique_ingredients = sorted(set(ingredient_list))

    return render_template('shopping_list.html', ingredients=unique_ingredients)"""


# Export Meal Plan as CSV
from flask import make_response
import csv
import io

@planner_bp.route('/meal-planner/export')
def export_meal_plan():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    plans = MealPlan.query.filter_by(user_id=user_id).all()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Day', 'Recipe Name', 'Ingredients'])

    for plan in plans:
        writer.writerow([plan.day_of_week, plan.recipe_name, plan.ingredients])

    response = make_response(output.getvalue())
    response.headers['Content-Disposition'] = 'attachment; filename=meal_plan.csv'
    response.headers['Content-type'] = 'text/csv'
    return response

