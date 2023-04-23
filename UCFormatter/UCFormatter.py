from dash import Dash, dcc, html, Input, Output, State, ctx
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import dash
import json
import requests
import redis
import subprocess
import atexit

from dash_helpers import *

# Making requests is OK because this is a public repo
UCFs_folder = 'https://raw.githubusercontent.com/CIDARLAB/Cello-UCF/develop/files/v2'
schema_link = 'https://raw.githubusercontent.com/CIDARLAB/Cello-UCF/develop/schemas/v2'

# Retrieves ucf-list
ucf_list = ['empty']
ucf_txt_path = 'UCFs/ucf-list.txt'
try:
    with open(ucf_txt_path, 'r') as f:
        file_contents = f.read()
        lines = file_contents.split('\n')
        lines = list(filter(lambda x: x != '', lines))
        ucf_list = lines
except Exception as e:
    debug_print(str(e))
    ucf_list = ['failed to read ucf-list file'] 
    
# set up in-memory caching for variables w redis
r = redis.Redis(host='localhost', port=6379, db=0)

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
# external_stylesheets += [dbc.themes.CYBORG]
app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(
    className='dark-theme',
    children=[
        dcc.Store(id='open-schema', data=None),

        html.H1(
            children='CELLO-V3',
            style={
                'textAlign': 'center',
                'color': '#0073e5',
                'flex': 1,
                'backgroundColor': '#afafaf',
                'height': 'max-height',
            }
        ),
        html.H3(
            '''UCFormatter Tool''',
            style={'flex': 1, 'textAlign': 'center', },
        ),
        html.Br(),

        html.Div(
            children=[
                html.Div(style={'flex': 0.2, 'textAlign': 'center'}),
                html.Div(
                    '''
                    The Cello software designs the DNA sequences for programmable circuits 
                    based on a high-level software description and a library of characterized 
                    DNA parts representing Boolean logic gates.
                    The user constraints file (UCF) is
                    a JavaScript Object Notation (JSON) file that describes 
                    a part and gate library for a particular organism.
                    ''',
                    style={'flex': 0.6, 'textAlign': 'center'},
                ),
                html.Div(style={'flex': 0.2, 'textAlign': 'center'}),
            ],
            style={
                'display': 'flex',
                'flex-direction': 'row',
            }
        ),
        html.Br(),

        html.Div(
            children=[
                html.Label('Select UCF template'),
                html.Div(
                    children=[
                        html.Div(
                            children=[
                                dcc.Dropdown(
                                    ucf_list, ucf_list[0], id='ucf-select'),
                                html.Br(),
                            ],
                            style={'flex': 1}
                        ),
                        html.Button(
                            '1. select UCF',
                            id='confirm-select',
                            style={'padding-bottom': -50}
                        ),
                    ], style={
                        'display': 'flex',
                        'align-items': 'stretch',
                        'flex-direction': 'row',
                        'padding-left': '100px',
                        'padding-right': '100px',
                    }
                ),
            ],
            style={
                'textAlign': 'center',
            }
        ),
        html.Div(
            [
                html.H5('UCF preview: '),
                html.Div(
                    dcc.RangeSlider(
                        id='ucf-range-slider',
                        min=0,
                        max=30,
                        step=1,
                        value=[0, 10],
                        pushable=10,
                        drag_value=[1],
                        marks=None,
                        tooltip={'placement': 'bottom'},
                    ),
                    style={
                        'padding-left': '100px',
                        'padding-right': '100px'
                    }
                ),
                html.Div(
                    children=generate_ucf_preview(),
                    id='ucf-preview',
                    style={
                        'padding-left': '100px',
                        'padding-right': '100px'
                    }
                ),
                # daq.Indicator(
                #     id='indicator-light',
                #     value=True,
                #     color='red'
                # ),
                html.Br(),
                html.Br(),
                html.Button(
                    '2. confirm selection',
                    id='refresh-page',
                ),
                html.Br(),
                html.Br(),
                html.Label("Choose a collection to modify"),
                html.Div(
                    [
                        html.Div(style={'flex': 0.3}),
                        html.Br(),
                        dcc.Dropdown(
                            ucf_list,
                            ucf_list[0],
                            id='collection-select',
                            style={
                                'flex': 0.4,
                            }
                        ),
                        html.Div(style={'flex': 0.3}),
                    ],
                    style={
                        'display': 'flex',
                        'flex-direction': 'row',
                        'alignItems': 'center',
                    }
                ),
                html.Br(),
            ],
            style={
                'text-align': 'center',
            }
        ),

        html.Div(
            children=[
                html.Div(
                    id='schema-preview',
                    style={
                        'flex':0.5,
                        'max-width': '50%',
                    }
                ),
                html.Div(style={'flex': 0.01}),
                html.Div(
                    id='schema-preview-2',
                    children=[
                        generate_schema_preview()
                    ],
                    style={
                        'flex':0.5
                    }
                ),
            ],
            style={
                'display': 'flex',
                'flex-direction': 'row',
                'alignItems': 'center',
                'padding-left': '100px',
                'padding-right': '100px'
            }
        ),

        html.Br(),
        html.Div(
            id='schema-input-form',
            children='placeholder',
            style={
                'padding-left': '100px',
                'padding-right': '100px'
            }
        ),
        html.Br(),

        html.Div(
            children=[
                html.H5('Modified Preview: '),
                # dcc.RangeSlider(
                #     id='ucf-range-slider-2',
                #     min=0,
                #     max=30,
                #     step=1,
                #     value=[0, 10],
                #     pushable=10,
                #     drag_value=[1],
                #     marks=None,
                #     tooltip={'placement': 'bottom'},
                # ),
                html.Div(
                    children=generate_ucf_preview(),
                    id='ucf-preview-2',
                ),
                html.Br(),
                html.Button(
                    'SUBMIT',
                    id='submit-modification',
                    # style={'padding-bottom': -50}
                ),
            ],
            style={
                'padding-left': '100px',
                'padding-right': '100px',
                'text-align': 'center',
            }
        ),
        html.Br(),

    ],
    style={
        'display': 'flex',
        'flex-direction': 'column',
    },
)

# CALLBACKS SECTION


@app.callback(
    Output('ucf-range-slider', 'disabled'),
    Output('ucf-preview', 'children'),
    Output('ucf-preview-2', 'children'),
    Output('ucf-range-slider', 'value'),
    Output('ucf-range-slider', 'max'),
    Input('confirm-select', 'n_clicks'),
    Input('ucf-range-slider', 'value'),
    State('ucf-select', 'value'),
    State('ucf-range-slider', 'disabled')
)
# NOTE: generate UCF preview and sets slider value
def preview_ucf(selectedUCF, slider_value, ucf_name, slider_disabled):
    slider_value = slider_helper(slider_value)
    ucf_path = UCFs_folder + '/'
    ucf_parse = ucf_name.split('.')
    ucf_path += ucf_parse[1].lower() + '/'
    # TODO: method needs update when UCF list expands
    ucf_pre = ucf_parse[0]
    group_name = ''
    if ucf_pre[0] == 'S':
        group_name = ucf_pre[:2]
    else:
        group_name = ucf_pre[:3]
    ucf_path += group_name
    try:
        with requests.get(f'{ucf_path}/{ucf_name}') as response:
            if response.ok:
                ucf_data = json.loads(response.content)
                r.set('ucf', response.content.decode())
                print('\'Click\'')
                print(json.dumps(ucf_data[0], indent=4))
                return False, generate_ucf_preview(ucf_data, slider_value), generate_ucf_preview(ucf_data), slider_value, len(ucf_data)
            else:
                print(ucf_path)
                debug_print(f'failed to retrieve {ucf_name}, error code ' + str(response.status_code))
                return True, generate_ucf_preview(), generate_ucf_preview(), slider_value, 30
    except Exception as e:
        debug_print(f'failed to retrieve {ucf_name}, exception: ')
        debug_print(e)
        return True, generate_ucf_preview(), generate_ucf_preview(), slider_value, 30


@app.callback(
    Output('collection-select', 'options'),
    Output('collection-select', 'value'),
    Input('refresh-page', 'n_clicks'),
    Input('confirm-select', 'n_clicks'),
    Input('ucf-select', 'value'),
)
# NOTE: updates the collection dropdown items when confirm-selction is clicked
# TODO: is it absolutely necessary?
# DEFAULT: msg, causes 404 for schema retrieval
def update_collections_dropdown(refresh_clicks, confirm_clicks, ucf_name):
    triggered_id = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    if triggered_id == 'confirm-select':
        return ['please confirm selection again.'], ''
    else:
        if refresh_clicks is not None:
            ucf = json.loads(r.get("ucf"))
            collections = []
            for c in ucf:
                collections.append(c["collection"])
            collections = list(set(collections))
            # options = [{'label': c, 'value': c} for c in collections]
            # return options
            return collections, ' '
        else:
            return ['first, confirm selection'], ''


@app.callback(
    Output('refresh-page', 'style'),
    [Input('refresh-page', 'n_clicks'),
     Input('confirm-select', 'n_clicks')],
    [State('refresh-page', 'style')]
)
# NOTE: click on confirm-select btn to make it green, and turns red whenever ucf btn is clicked
# makes sure that the
def autobots_roll_out(refresh_clicks, confirm_clicks, color):
    triggered_id = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    debug_print(triggered_id)
    if triggered_id == 'confirm-select':
        # {'background-color': '#d62d20'}
        return {'background-color': '#fa3c4c'}
    elif refresh_clicks is not None:
        ucf = json.loads(r.get("ucf"))
        collections = []
        for c in ucf:
            collections.append(c["collection"])
        collections = list(set(collections))
        display = []
        for c in collections:
            display.append(html.Li(c))
        return {'background-color': '#7ddc1f'} # green 
    else:
        return {'background-color': '#fa3c4c'} # red 


@app.callback(
    Output('schema-preview', 'children'),
    Output('schema-input-form', 'children'),
    Output('open-schema', 'data'),
    Output('schema-preview-2','children'),
    Input('collection-select', 'options'),
    Input('collection-select', 'value'),
    State('refresh-page', 'style'),
)
def preview_schema(c_options, c_name, confirm_btn_color):
    debug_print('c_options\n' + str(c_options))
    schema1 = generate_schema_preview()
    inputForm = 'placeholder'
    schemaData = None
    schema2 = generate_schema_preview()
    print(confirm_btn_color)
    if c_name not in c_options or confirm_btn_color['background-color'] == '#fa3c4c':
        return schema1, inputForm, schemaData, schema2
    try:
        with requests.get(schema_link+'/'+str(c_name)+'.schema.json') as response:
            if response.ok:
                # r.set(c_name, response.content.decode())
                schemaData = json.loads(response.content)
                print('\'Click\'')
                print(json.dumps(schemaData, indent=4))
                schema1 = generate_schema_preview(schemaData)
                inputForm = generate_input_components(schemaData['properties'])
            else:
                debug_print('Could not complete response to retrieve schema')
                debug_print(str(response.status_code))
    except Exception as e:
        debug_print('Exception with completing response')
        debug_print(str(e))
    try:
        collection_list = find_collection_in_ucf(c_name, json.loads(r.get("ucf")))
        schema2 = generate_schema_preview(collection_list)
    except Exception as e:
        debug_print('Exception finding collection name in UCF file')
        debug_print(str(e))
    return schema1, inputForm, schemaData, schema2


if __name__ == '__main__':
    start_redis_server()
    atexit.register(stop_redis_server)
    app.run_server(debug=True)
