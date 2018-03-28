# main.py

from app import app
from forms import ProductSelectForm
from flask import flash, render_template, request, redirect
import json
from product import run_ims 

# init_db()


@app.route('/', methods=['GET', 'POST'])
def index():
    form = ProductSelectForm(request.form)
    if request.method == 'POST':
        return search_results(form)

    return render_template('index.html', form=form)


@app.route('/results')
def search_results(form):
    results = {}
    output = run_ims(form)


    if not output:
        flash('No results found!')
        return redirect('/')
    else:
        # display results
        return render_template('results.html' , results = output ) #results=json.dumps(results))

if __name__ == '__main__':
    import os
    if 'WINGDB_ACTIVE' in os.environ:
        app.debug = False
    app.debug = True
    app.run(port=5003)
