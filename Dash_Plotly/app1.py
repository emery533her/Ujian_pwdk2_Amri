import os

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from plotly import tools
from dash.dependencies import Input, Output
# from categoryplot import dfTips, getPlot
import numpy as np
from sqlalchemy import create_engine

engine = create_engine(
    "mysql+mysqlconnector://root:cinta1malam@localhost/ujiantitanic?host=localhost?port=3306")
conn = engine.connect()


def panggil(k):
    q = f'''SELECT * FROM {k}'''
    results = conn.execute(q).fetchall()
    df1 = pd.DataFrame(results)
    df1.columns = results[0].keys()
#     df1.set_index('id', inplace=True)
    return df1


listGOFunc = {
    "bar": go.Bar,
    "violin": go.Violin,
    "box": go.Box
}


def getPlot(jenis, xCategory):
    df = panggil('titanic')
    return [listGOFunc[jenis](
        x=df[xCategory],
        y=df['fare'],
        opacity=0.7,
        name='Fare',
        marker=dict(color='blue'),
        legendgroup='Fare'
    ),
        listGOFunc[jenis](
        x=dfTips[xCategory],
        y=dfTips['age'],
        opacity=0.7,
        name='Age',
        marker=dict(color='orange'),
        legendgroup='Age'
    )]


dfTips = panggil('titanic')

app = dash.Dash(__name__)
server = app.server  # make python obj with Dash() method

color_set = {
    'sex': ['#ff3fd8', '#4290ff'],
    'smoker': ['#32fc7c', '#ed2828'],
    'time': ['#0059a3', '#f2e200'],
    'day': ['#ff8800', '#ddff00', '#3de800', '#00c9ed']
}

estiFunc = {
    'count': len,
    'sum': sum,
    'mean': np.mean,
    'std': np.std
}

disabledEsti = {
    'count': True,
    'sum': False,
    'mean': False,
    'std': False
}

subplots_hist = {
    'sex': [1, 2],
    'smoker': [1, 2],
    'time': [1, 2],
    'day': [2, 2]
}

app.title = 'Ujian Purwadhika'  # set web title


def getMaxAndMinBoundary(col):
    return {
        'max': dfTips[col].mean() + dfTips[col].std(),
        'min': dfTips[col].mean() - dfTips[col].std()
    }

# function to generate HTML Table


def generate_table(dataframe, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col, className='table_dataset') for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col], className='table_dataset') for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))], className='table_dataset'
    )


# the layout/content
app.layout = html.Div(children=[
    dcc.Tabs(id="tabs", value='tab-1',
             style={
                 'fontFamily': 'system-ui'
             },
             content_style={
                 'fontFamily': 'Arial',
                 'borderLeft': '1px solid #d6d6d6',
                 'borderRight': '1px solid #d6d6d6',
                 'borderBottom': '1px solid #d6d6d6',
                 'padding': '44px'
             },
             children=[
                 dcc.Tab(label='Tips Data Set', value='tab-1', children=[
                     html.Div([
                         html.H1('Tips Data Set'),
                         dcc.Dropdown(
                             id='inp_drop',
                             options=[{'label': 'Titanic', 'value': 'titanic'},
                                      {'label': 'Titanic Outlier Calculation', 'value': 'titanicoutcalc'}],
                             value='titanic'
                         ),
                         html.Div(id='isitab1', children=[])
                     ])
                 ]),
                 dcc.Tab(label='Categorical Plot', value='tab-3', children=[
                     html.Div([
                         html.H1('Categorical Plot Tips Data Set'),
                         html.Table([
                             html.Tr([
                                 html.Td([
                                     html.P('Jenis : '),
                                     dcc.Dropdown(
                                         id='ddl-jenis-plot-category',
                                         options=[{'label': 'Bar', 'value': 'bar'},
                                                  {'label': 'Violin',
                                                      'value': 'violin'},
                                                  {'label': 'Box', 'value': 'box'}],
                                         value='bar'
                                     )
                                 ]),
                                 html.Td([
                                     html.P('X Axis : '),
                                     dcc.Dropdown(
                                         id='ddl-x-plot-category',
                                         options=[{'label': 'Survived', 'value': 'survived'},
                                                  {'label': 'Sex', 'value': 'sex'},
                                                  {'label': 'Ticket Class',
                                                   'value': 'ticket_class'},
                                                  {'label': 'Embark Town',
                                                   'value': 'embark_town'},
                                                  {'label': 'Who', 'value': 'who'},
                                                  {'label': 'Outlier', 'value': 'outlier'}],
                                         value='sex'
                                     )
                                 ])
                             ])
                         ], style={'width': '700px', 'margin': '0 auto'}),
                         dcc.Graph(
                             id='categoricalPlot',
                             figure={
                                 'data': []
                             }
                         )
                     ])
                 ]),
             ])
],
    style={
    'maxWidth': '1000px',
    'margin': '0 auto'
})

# prototype callback
# @app.callback(
#     Output('text_min_max', 'children'),
#     [Input('inp_slider', 'value')]
# )
# def update_scatter_jmlData(inp_slider):
#     return f'Range Total Bill {inp_slider}'


@app.callback(
    Output('categoricalPlot', 'figure'),
    [Input('ddl-jenis-plot-category', 'value'),
     Input('ddl-x-plot-category', 'value')])
def update_category_graph(ddljeniscategory, ddlxcategory):
    return {
        'data': getPlot(ddljeniscategory, ddlxcategory),
        'layout': go.Layout(
            xaxis={'title': ddlxcategory.capitalize()}, yaxis={'title': 'US$'},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 0, 'y': 1.2}, hovermode='closest',
            boxmode='group', violinmode='group'
            # plot_bgcolor= 'black', paper_bgcolor= 'black',
        )
    }


if __name__ == '__main__':
    # run server on port 1997
    # debug=True for auto restart if code edited
    app.run_server(debug=True, port=1997)
