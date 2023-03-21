from dash import Dash, dcc, html, Input, Output, State, ctx
from dash.exceptions import PreventUpdate
import dash
import json
import requests
import redis
import subprocess
import math

# TODO: refactor code

# automatically starting Redis, may be disabled

def debug_print(msg):
    print(f'\nDEBUG: {msg}\n')

def start_redis_server():
    cmd = ['redis-cli', 'ping']
    try:
        subprocess.check_output(cmd)
        print('Redis server is already running.')
        return
    except Exception as e:
        debug_print(e)
        pass

    # Start Redis server
    cmd = ['redis-server']
    subprocess.Popen(cmd)
    print('Redis server started.')

def generate_ucf_preview(ucf=None, slider_range=None,):
    if ucf is None:
        return html.Div(
            'awaiting UCF initialization...',
            style={
                'min-height': '300px',
                'overflow': 'auto',
                'white-space': 'nowrap',
                'background-color': 'rgba(128, 128, 128, 0.1)',
                'display': 'flex',
                'align-items': 'center',
                'justify-content': 'center',
            }
        )
    slice = []
    if slider_range is None:
        slice = ucf[:10]
    else:
        slice = ucf[slider_range[0]:slider_range[1]]
    return html.Div(
        html.Pre(json.dumps(slice, indent=4)),
        style={
            'height': '500px',
            'overflow': 'auto',
            'white-space': 'nowrap',
            'background-color': 'rgba(128, 128, 128, 0.1)',
            'text-align': 'left'
        }
    )

# Making requests is OK because this is a public repo
UCFs_folder = 'https://raw.githubusercontent.com/ginomcfino/CELLO-3.0/main/UCFormatter/UCFs'
schema_link = 'https://raw.githubusercontent.com/CIDARLAB/Cello-UCF/develop/schemas/v2'

# Retrieves ucf-list
ucf_list = None
ucf_txt_url = UCFs_folder + '/ucf-list.txt'
try:
    ucf_resp = requests.get(ucf_txt_url)
    if ucf_resp.ok:
        file_contents = ucf_resp.content.decode('utf-8')
        lines = file_contents.split('\n')
        lines = list(filter(lambda x: x != '', lines))
        # print(lines)
        ucf_list = lines
    else:
        print(f"Failed to get file contents. Status code: {ucf_resp.status_code}")
except Exception as e:
    debug_print(str(e))
    ucf_list=['please researt the app once connected to internet']

# TODO: Implement AWS ElastiCache for in-memory storage (or Redis)

# set up in-memory caching for variables w redis
r = redis.Redis(host='localhost', port=6379, db=0)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(
    children=[
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
                html.Div(
                    id='schema-preview',
                    style={
                        'padding-left': '100px',
                        'padding-right': '100px'
                    }
                ),
            ],
            style={
                'text-align': 'center',
            }
        ),

        html.Br(),

        # signal value that triggers callbacks
        # dcc.Store('signal')

    ],
    style={
        'display': 'flex',
        'flex-direction': 'column',
        # for 'night mode'
        # 'backgroundColor': 'black',
        # 'color': 'white',
        # 'padding': '0'
    },
)


def generate_schema_preview(schema=None):
    if schema is None:
        return html.Div(
            'select a collection name to preview',
            style={
                'height': '300px',
                'overflow': 'auto',
                'white-space': 'nowrap',
                'background-color': 'rgba(128, 128, 128, 0.1)',
                'display': 'flex',
                'align-items': 'center',
                'justify-content': 'center',
            }
        )
    else:
        debug_print('loading schema')
        return html.Div(
            html.Pre(json.dumps(schema, indent=4)),
            style={
                'min-height': '300px',
                'overflow': 'auto',
                'white-space': 'nowrap',
                'background-color': 'rgba(128, 128, 128, 0.1)',
                'text-align': 'left'
            }
        )

@app.callback(
    Output('ucf-range-slider', 'disabled'),
    Output('ucf-preview', 'children'),
    Output('ucf-range-slider', 'value'),
    Output('ucf-range-slider', 'max'),
    Input('confirm-select', 'n_clicks'),
    Input('ucf-range-slider', 'value'),
    State('ucf-select', 'value'),
    State('ucf-range-slider', 'disabled')
)
# NOTE: save selected ucf into cache on ucf btn click
def preview_ucf(selectedUCF, slider_value, ucf_name, slider_disabled):
    if abs(slider_value[1] - slider_value[0]) != 10:
        if slider_value[1] > slider_value[0]:
            new_value = [slider_value[1] - 10, slider_value[1]]
        else:
            new_value = [slider_value[0], slider_value[0] + 10]
        slider_value = new_value
    try:
        with requests.get(UCFs_folder+'/'+ucf_name) as response:
            if response.ok:
                ucf_data = json.loads(response.content)
                r.set('ucf', response.content.decode())
                print('\'Click\'')
                print(json.dumps(ucf_data[0], indent=4))
                return False, generate_ucf_preview(ucf_data, slider_value), slider_value, len(ucf_data)
            else:
                return True, generate_ucf_preview(), slider_value, 30
    except:
        return True, generate_ucf_preview(), slider_value, 30


@app.callback(
    Output('collection-select', 'options'),
    [Input('refresh-page', 'n_clicks')],
)
# NOTE: updates the collection dropdown items when confirm-selction is clicked
# TODO: is it absolutely necessary?
# DEFAULT: msg, causes 404 for schema retrieval
def update_collections_dropdown(refresh):
    if refresh is not None:
        ucf = json.loads(r.get("ucf"))
        collections = []
        for c in ucf:
            collections.append(c["collection"])
        collections = list(set(collections))
        options = [{'label': c, 'value': c} for c in collections]
        return options
    else:
        return ['first, confirm selection']


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
    print(triggered_id)
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
        return {'background-color': '#7ddc1f'}
    else:
        return {'background-color': '#d62d20'}


# @app.callback(
#     Output('ucf-range-slider', 'value'),
#     Output('ucf-preview', 'children'),
#     Input('ucf-range-slider', 'value'),
# )
# # simply ensures the range slider for UCF does note go 
# def update_range_slider(value):
#     ucf = json.loads(r.get('ucf'))
#     if abs(value[1] - value[0]) != 10:
#         if value[1] > value[0]:
#             new_value = [value[1] - 10, value[1]]
#         else:
#             new_value = [value[0], value[0] + 10]
#         value = new_value
#     return value, generate_ucf_preview(ucf, value)


@app.callback(
    Output('schema-preview', 'children'),
    [Input('collection-select', 'value')],
)
def preview_schema(c_name):
    try:
        with requests.get(schema_link+'/'+str(c_name)+'.schema.json') as response:
            if response.ok:
                schema = json.loads(response.content)
                r.set('open-schema', response.content.decode())
                print('\'Click\'')
                print(json.dumps(schema, indent=4))
                return generate_schema_preview(schema)
            else:
                debug_print(str(response.status_code))
                debug_print('empty schema preview')
                return generate_schema_preview()
    except:
        return generate_schema_preview()


if __name__ == '__main__':
    start_redis_server()
    app.run_server(debug=True)