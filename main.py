# import plotly
import plotly.express as px

import pandas as pd
import numpy as np

from io import StringIO

from flask import Flask, render_template, request

import logging
logging.basicConfig(level=logging.DEBUG)


def create_unique_bar_graph(randomText, seperator):
    if randomText is None:
        randomText = '\t'.join([str(np.random.randn()) for i in range(10)])

    app.logger.info("Creating bar graph with: "+str(randomText))
    app.logger.info("Using seperator: "+str(seperator))

    # randomTextData = StringIO(randomText)
    # app.logger.info("StringIO got: "+str(randomTextData.getvalue()))
    #   read the textarea, convert everything to float64, ignore excess columns

    if seperator == "\\t":
        random_text_data_list = randomText.split("\t")
        # app.logger.info('Since TAB, use: "\t"')
    else:
        random_text_data_list = randomText.split(seperator)
        # app.logger.info("Since other seperator, use: "+seperator)

    app.logger.info("list length: " + str(len(random_text_data_list)))

    # for entry in random_text_data_list:
    #     app.logger.info("Each entry: " + str(entry))

    # intilize a null list
    unique_list = []

    # traverse for all elements
    for entry in random_text_data_list:
        # check if exists in unique_list or not
        if entry not in unique_list:
            unique_list.append(entry)

    # # print list
    # for entry in unique_list:
    #     app.logger.info("Each unique entry: " + str(entry))

    random_text_data_list_indexes = ''

    for entry in random_text_data_list:
        for unique_entry in unique_list:
            if entry == unique_entry:
                random_text_data_list_indexes += str(unique_list.index(unique_entry)+1)+"\t"

    app.logger.info("list into indexes: " + random_text_data_list_indexes)

    random_text_data_list_indexes_IO = StringIO(random_text_data_list_indexes)

    df = pd.read_csv(
        random_text_data_list_indexes_IO,
        header=None,
        sep="\t",
        index_col=False,
        error_bad_lines=False
        )
    app.logger.info("Dataframe read CSV: ")
    df.info()

    df = df.apply(pd.to_numeric, errors='coerce')
    df = df.astype("float64")
    df.fillna(0)
    app.logger.info("Datafram to numeric: ")
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


def create_bar_graph(randomText, seperator):
    if randomText is None:
        randomText = '\t'.join([str(np.random.randn()) for i in range(10)])

    app.logger.info("Creating bar graph with: "+str(randomText))
    randomTextData = StringIO(randomText)
    app.logger.info("StringIO got: "+str(randomTextData.getvalue()))
#   read the textarea, convert everything to float64, ignore excess columns

    df = pd.read_csv(
        randomTextData,
        header=None,
        sep=seperator,
        index_col=False,
        error_bad_lines=False
        )
    app.logger.info("Dataframe read CSV: ")
    df.info()

    df = df.apply(pd.to_numeric, errors='coerce')
    df = df.astype("float64")
    df.fillna(0)
    app.logger.info("Datafram to numeric: ")
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


def create_scatter(randomText, seperator):
    if randomText is None:
        randomText = '\t'.join([str(np.random.randn()) for i in range(10)])

    app.logger.info("Creating scatter plot with:"+str(randomText))
    randomTextData = StringIO(randomText)
    app.logger.info("StringIO got:"+randomTextData.getvalue())
#   read the textarea, convert everything to float64, ignore excess columns
    df = pd.read_csv(
        randomTextData,
        header=None,
        sep=seperator,
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
    seperator = request.form.get('seperator')
    randomText = request.form.get('textArea')
    app.logger.info('text area form got: '+str(randomText))
    uniqueBarGraph = create_unique_bar_graph(randomText, seperator)
    barGraph = create_bar_graph(randomText, seperator)
    scatterPlot = create_scatter(randomText, seperator)

    if request.method == 'POST':
        app.logger.info('POSTED')

    return render_template(
        'index.html',
        barGraph=barGraph,
        scatterPlot=scatterPlot,
        uniqueBarGraph=uniqueBarGraph)


if __name__ == "__main__":
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host='127.0.0.1', port=5000, debug=True)
