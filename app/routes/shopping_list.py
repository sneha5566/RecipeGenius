from flask import Blueprint, render_template, session, redirect, url_for
from app.models import ShoppingItem

shopping_bp = Blueprint('shopping', __name__)

@shopping_bp.route('/shopping-list')
def shopping_list():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    print("SESSION USER_ID:", user_id)

    # ✅ Fetch items from DB
    items = ShoppingItem.query.filter_by(user_id=user_id).all()
    print("ITEM COUNT:", len(items))

    grouped = {}

    for item in items:
        day = item.day_of_week or "Unspecified"
        ingredient = item.ingredient_name.strip().capitalize()
        grouped.setdefault(day, set()).add(ingredient)

    # ✅ Convert sets to sorted lists
    for day in grouped:
        grouped[day] = sorted(grouped[day])

    print("DEBUG grouped:", grouped)

    return render_template("shopping_list.html", grouped_ingredients=grouped)

@shopping_bp.route('/download_csv')
def download_csv():
    from flask import make_response
    import csv
    import io

    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    items = ShoppingItem.query.filter_by(user_id=user_id).all()

    # Group ingredients by day
    grouped_ingredients = {}
    for item in items:
        day = item.day_of_week or "Unspecified"
        ingredient = item.ingredient_name.strip().capitalize()
        grouped_ingredients.setdefault(day, set()).add(ingredient)

    # Convert sets to sorted lists
    for day in grouped_ingredients:
        grouped_ingredients[day] = sorted(grouped_ingredients[day])

    # Prepare CSV response
    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow(['Day', 'Ingredients'])
    for day, ingredients in grouped_ingredients.items():
        writer.writerow([day, ', '.join(ingredients)])

    response = make_response(output.getvalue())
    response.headers['Content-Disposition'] = 'attachment; filename=shopping_list.csv'
    response.headers['Content-type'] = 'text/csv'
    return response

