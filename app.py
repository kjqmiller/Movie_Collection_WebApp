import json
from flask import Flask, render_template, request
from helpers import query_imdb, save_to_db, get_all_titles, delete_from_db
from pprint import pprint

app = Flask(__name__)


# TO START
# source env/bin/activate

# ROUTES
# HOME ROUTE
# TODO Contains search button, will eventually have this at the top of every page along with other nav buttons
@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')


# COLLECTION ROUTE
@app.route('/collection', methods=['GET'])
def collection():
    titles = get_all_titles()
    return render_template('collection.html', titles=titles)


# RESULTS ROUTE
# Render page with results from search, letting the user select whichever titles they want
@app.route('/results', methods=['POST'])
def results():
    if request.method == 'POST':
        # Get text entered in form with text input and run search function
        search_query = request.form['search_query']

        # If nothing is entered, reload page, else load results.html and pass the returned titles as 'title'
        if search_query == '':
            return render_template('index.html', empty=True)
        else:
            query_return = query_imdb(search_query)
            return render_template('results.html', titles=query_return)


# SUBMIT ROUTE
# Handles submission of form from results route, redirects back to home page after success or failure
@app.route('/submit', methods=['POST'])
def submit():
    titles = []
    if request.method == 'POST':
        selected_ids = request.form.getlist('checked_title')
        # Python string uses single quote ' whereas json uses double ", had to replace to make json.loads() work
        for item in selected_ids:
            pprint(item)
            item = item.replace('\'', '\"')
            try:
                title = json.loads(item)
                titles.append(title)
            except ValueError:
                return render_template('index.html', success=2)
    try:
        save_to_db(titles)
        return render_template('index.html', success=0)
    except Exception:
        return render_template('index.html', success=1)


# DELETE ROUTE
@app.route('/delete', methods=['POST'])
def delete():
    # Get title id and pass to pymongo delete helper function
    try:
        if request.method == 'POST':
            title_to_delete = request.form.get('delete')
            title_to_delete = title_to_delete.replace('\'', '\"')
            pprint(title_to_delete)
            delete_from_db(title_to_delete)
        return render_template('index.html', deleted=True)
    except Exception:
        return render_template('index.html', deleted=False)


if __name__ == '__main__':
    app.run(debug=True)  # Errors pop up on page
