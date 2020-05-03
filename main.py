# import plotly
import plotly.express as px
import plotly.graph_objects as go

import pandas as pd
import numpy as np

from flask import Flask, render_template, request


def create_bar_graph(quantity):
    # sending the JSON of the graph object to plotly javascript front end as
    # .newPlot(div, object)
    if quantity is None:
        quantity = 10
    N = int(quantity)
    x = np.linspace(0, 1, N)
    y = np.random.randn(N)

    # df = pd.DataFrame({'x': x, 'y': y})

    fig = go.Figure(
        data=[go.Bar(x=x, y=y)])

    figJSON = fig.to_json()

    return figJSON


def create_bar_graph_from_object(elementID, quantity):
    if quantity is None:
        quantity = 10
    N = int(quantity)
    x = np.linspace(0, 1, N)
    y = np.random.randn(N)

    # df = pd.DataFrame({'x': x, 'y': y})

    fig = go.Figure(
        data=[go.Bar(x=x, y=y)],
        layout=go.Layout(
            title=go.layout.Title(
                text="A Figure Specified By A Graph Object")))

    JSONdata = fig.to_json()

    jsTextStart = '<script>Plotly.newPlot('
    jsLayout = ',{"title": "Hide the Modebar"}'
    jsConfig = ',{"displayModeBar": false, "responsive": true}'
    jsTextEnd = ');</script>'

    jsToInsert = jsTextStart+elementID+","+JSONdata+jsLayout+jsConfig+jsTextEnd

    return jsToInsert


def create_bar_using_express(elementID, quantity):
    if quantity is None:
        quantity = 10
    N = int(quantity)
    x = np.linspace(0, 1, N)
    y = np.random.randn(N)
    df = pd.DataFrame({'x': x, 'y': y})

    fig = px.bar(
        df,
        x='x',
        y='y',
        title="A Plotly Express Figure"
        )

    JSONdata = fig.to_json()

    jsTextStart = '<script>Plotly.newPlot('
    jsLayout = ',{"title": "Hide the Modebar"}'
    jsConfig = ',{"displayModeBar": false, "responsive": true}'
    jsTextEnd = ');</script>'

    jsToInsert = jsTextStart+elementID+","+JSONdata+jsLayout+jsConfig+jsTextEnd

    return jsToInsert


def create_scatter(elementID, quantity):
    if quantity is None:
        quantity = 10
    N = int(quantity)
    x = np.random.randn(N)
    xFactors = x
    y = np.random.randn(N)
    df = pd.DataFrame({'x': x, 'y': y, 'colors': xFactors})

    data = px.scatter(
        df,
        x='x',
        y='y',
        color='colors',
        marginal_y="rug",
        marginal_x="histogram"
        )

    JSONdata = data.to_json()

    jsTextStart = '<script>Plotly.newPlot('
    jsTextEnd = ',{});</script>'
    jsToInsert = jsTextStart+elementID+','+JSONdata+jsTextEnd

    return jsToInsert


def testFunction():
    test = 'TEST {}'
    return test


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    quantity = request.form.get('quantityValue')
    barGraph = create_bar_graph(quantity)
    scatterPlot = create_scatter("'scatterPlot'", quantity)
    test = testFunction()

    if request.method == 'POST':
        test += 'POSTED'

    return render_template(
        'index.html',
        barGraph=barGraph,
        scatterPlot=scatterPlot,
        test=test)


if __name__ == "__main__":
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host='127.0.0.1', port=5000, debug=True)
