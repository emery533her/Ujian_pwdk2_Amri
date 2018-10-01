import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from plotly import tools
from dash.dependencies import Input, Output
import numpy as np

# pydata stack
import pandas as pd
from sqlalchemy import create_engine

# set params
engine = create_engine(
    "mysql+mysqlconnector://root:cinta1malam@localhost/ujiantitanic?host=localhost?port=3306")
conn = engine.connect()

app = dash.Dash(__name__)
server = app.server  # make python obj with Dash() method

app.title = 'Templates'

#######################
# Data Analysis / Model
#######################


def panggil(k):
    q = f'''SELECT * FROM {k}'''
    results = conn.execute(q).fetchall()
    df = pd.DataFrame(results)
    df.columns = results[0].keys()
#     df1.set_index('id', inplace=True)
    return df


# test
df = panggil('titanic')

#########################
# Dashboard Layout / View
#########################


# Set up Dashboard and create layout
app = dash.Dash()
# app.css.append_css({
#     "external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"
# })

app.layout = html.Div([
    html.Tabs(id='tabs', value='tab-1', children=[
        html.Tab(label='Ujian Titanic Dataset', value='tab-1', children=[

        ])
    ])
])


#############################################
# Interaction Between Components / Controller
#############################################

# A callback to return text under the dropdown
# @app.callback(
#     Output(component_id='teks1', component_property='children'),
#     [
#         Input(component_id='ddl', component_property='value')
#     ]
# )
# def ctrl_func(ddl):
#     return html.P('What to do with the number: ' + '<b>'+str(ddl)+'</b>')


# @app.callback(
#     Output(component_id='ddl2', component_property='options'),
#     [
#         Input(component_id='ddl', component_property='value')
#     ]
# )
# def ctrl_func1(ddl):
#     return [{'label': i, 'value': i} for i in optiDict[ddl]]


# start Flask server
if __name__ == '__main__':
    app.run_server(debug=True)
