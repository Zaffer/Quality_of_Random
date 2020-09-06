# import plotly
import plotly.express as px

import pandas as pd
import numpy as np

from io import StringIO

from flask import Flask, render_template, request

import logging
logging.basicConfig(level=logging.DEBUG)


def create_bar_graph(randomText):
    if randomText is None:
        randomText = '\t'.join([str(np.random.randn()) for i in range(10)])

    app.logger.info("Creating bar graph with:"+str(randomText))
    randomTextData = StringIO(randomText)
    app.logger.info("StringIO got:"+randomTextData.getvalue())
#   read the textarea, convert everything to float64, ignore excess columns
    df = pd.read_csv(
        randomTextData,
        header=None,
        sep="\t",
        index_col=False,
        error_bad_lines=False
        )
    df = df.apply(pd.to_numeric, errors='coerce')
    df = df.astype("float64")
    df.fillna(0)
    app.logger.info("Datafram info:")
    df.info()

    fig = px.bar(df)

#       #create figure from Graph Objects (needs import plotly graph objects)
#     df = pd.DataFrame({'x': x, 'y': y})

#     fig = go.Figure(
#         data=[go.Bar(x=x, y=y)],
#         layout=go.Layout(
#             title=go.layout.Title(
#                 text="A Figure Specified By A Graph Object")))

    figJSON = fig.to_json()

    return figJSON


def create_scatter(randomText):
    if randomText is None:
        randomText = '\t'.join([str(np.random.randn()) for i in range(10)])

    app.logger.info("Creating scatter plot with:"+str(randomText))
    randomTextData = StringIO(randomText)
    app.logger.info("StringIO got:"+randomTextData.getvalue())
#   read the textarea, convert everything to float64, ignore excess columns
    df = pd.read_csv(
        randomTextData,
        header=None,
        sep="\t",
        index_col=False,
        error_bad_lines=False
        )
    df = df.apply(pd.to_numeric, errors='coerce')
    df = df.astype("float64")
    df.fillna(0)
    app.logger.info("Datafram info:")
    df.info()

    fig = px.scatter(df)

    figJSON = fig.to_json()

    return figJSON


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    app.logger.info('-------LOGGER DEBUG-------')
    randomText = request.form.get('textArea')
    app.logger.info('text area form got:'+str(randomText))
    barGraph = create_bar_graph(randomText)
    scatterPlot = create_scatter(randomText)

    if request.method == 'POST':
        app.logger.info('POSTED')

    return render_template(
        'index.html',
        barGraph=barGraph,
        scatterPlot=scatterPlot)


if __name__ == "__main__":
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host='127.0.0.1', port=5000, debug=True)
