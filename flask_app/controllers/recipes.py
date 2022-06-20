from flask_app import app
from flask import redirect, render_template, request, session
from flask_app.models.recipe import Recipe


@app.route('/recipes/<int:id>')
def show_recipe(id):
    recipe_to_show = Recipe.get_recipe_by_id(id)
    return render_template('recipe.html', recipe_to_show=recipe_to_show)

@app.route('/add_recipe', methods=['GET','POST'])
def add_recipe():
    if 'user_id' not in session:
        return redirect('/logout')
    if request.method == 'GET':
        return render_template('recipe.html')
    else:
        if not Recipe.validate_recipe(request.form):
            return redirect('/add_recipe')
        data= {
                'name' : request.form['name'],
                'description' : request.form['description'],
                'instructions' : request.form['instructions'],
                'date_made' : request.form['date_made'],
                'under30min' : request.form['under30min'],
                'user_id' : session['user_id']
            }
        Recipe.add_recipe(data)
        return redirect('/dashboard')

@app.route('/view_recipe/<int:id>')
def view_recipe(id):
    if 'user_id' not in session:
        return redirect('/logout')
    recipe_to_view = Recipe.get_recipe_by_id(id)
    return render_template('view_recipe.html', recipe_to_view=recipe_to_view)

@app.route('/edit_recipe/<int:id>', methods=['GET', 'POST'])
def edit_recipe(id):
    if 'user_id' not in session:
        return redirect('/logout')
    recipe_to_edit= Recipe.get_recipe_by_id(id)
    if request.method == 'GET':
        return render_template('edit_recipe.html', recipe_to_edit=recipe_to_edit)
    else:
        if not Recipe.validate_recipe(request.form):
            return redirect('/edit_recipe/' + str(recipe_to_edit.id))
        Recipe.edit_recipe(request.form)
        return redirect('/dashboard')

@app.route('/delete_recipe/<int:id>')
def delete_recipe(id):
    if 'user_id' not in session:
        return redirect('/logout')
    Recipe.delete_recipe(id)
    return redirect('/dashboard')