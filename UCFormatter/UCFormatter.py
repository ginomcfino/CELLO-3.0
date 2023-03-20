from dash import Dash, dcc, html, Input, Output, State
from dash.exceptions import PreventUpdate
import json
import requests
import redis
import subprocess

# NOTE: automatically starting Redis, may be disabled
def start_redis_server():
    cmd = ['redis-cli', 'ping']
    try:
        subprocess.check_output(cmd)
        print('Redis server is already running.')
        return
    except:
        pass

    # Start Redis server
    cmd = ['redis-server']
    subprocess.Popen(cmd)
    print('Redis server started.')


# Making requests is OK because this is a public repo
UCFs_folder = 'https://raw.githubusercontent.com/ginomcfino/CELLO-3.0/main/UCFormatter/UCFs'

# TODO: link schemas from the schemas folder
# schema_link = 'https://github.com/CIDARLAB/Cello-UCF/develop/schemas/v2/<xxx.schema.json>'

# Retrieves ucf-list
ucf_list = None
ucf_txt_url = UCFs_folder + '/ucf-list.txt'
ucf_resp = requests.get(ucf_txt_url)
if ucf_resp.ok:
    file_contents = ucf_resp.content.decode('utf-8')
    lines = file_contents.split('\n')
    lines = list(filter(lambda x: x != '', lines))
    # print(lines)
    ucf_list = lines
else:
    print(f"Failed to get file contents. Status code: {ucf_resp.status_code}")

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
                'color': '#111111',
                'flex': 1,
                'backgroundColor': 'grey',
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
                html.Label('Select UCF template: '),
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
                            'Confirm',
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
                    id='ucf_preview',
                    style={
                        'padding-left': '100px',
                        'padding-right': '100px'
                    }
                ),
                html.Br(),
                html.Button(
                    'refresh',
                    id='refresh-page',
                ),
                html.Br(),
                html.Div(id='ucf_collection_names'),
                html.Br(),
                "Please select a collection to modify ",
                html.Div(
                    [
                        html.Div(style={'flex':0.3}),
                        
                        html.Br(),
                        dcc.Dropdown(
                                    ucf_list, 
                                    ucf_list[0], 
                                    id='collection-select',
                                    style= {
                                        'flex' : 0.4,
                                    }
                        ),
                        html.Div(style={'flex':0.3}),
                        # dcc.Input(id='ucf_choice', value='-----', type='text'),
                        # html.Button(id='pick_ucf_button',
                        #             n_clicks=0, children='Submit')
                    ],
                    style={
                        'display':'flex',
                        'flex-direction': 'row',
                        'alignItems': 'center',
                    }
                ),
            ],
            style={
                'text-align': 'center',
            }
        ),

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


@app.callback(
    Output('ucf_preview', 'children'),
    Input('confirm-select', 'n_clicks'),
    State('ucf-select', 'value')
)
def select_ucf(_, ucf_name):
    with requests.get(UCFs_folder+'/'+ucf_name) as response:
        if response.ok:
            ucf_data = json.loads(response.content)
            r.set('ucf', response.content.decode())
            print('\'Click\'')
            print(json.dumps(ucf_data[0], indent=4))
        else:
            raise PreventUpdate
    return html.Div(
        html.Pre(json.dumps(ucf_data[:10], indent=4)),
        style={
            'height': '500px',
            'overflow': 'auto',
            'white-space': 'nowrap',
            'background-color': 'rgba(128, 128, 128, 0.1)',
            'text-align': 'left'
        }
    )


@app.callback(
    Output('ucf_collection_names', 'children'),
    [Input('refresh-page', 'n_clicks')],
)
def wibblewobble(clicks):
    if clicks is not None:
        ucf = json.loads(r.get("ucf"))
        collections = []
        for c in ucf:
            collections.append(c["collection"])
        collections = list(set(collections))
        display = []
        for c in collections:
            display.append(html.Li(c))
        return html.Ul(display)
    else:
        return ''


if __name__ == '__main__':
    start_redis_server()
    app.run_server(debug=True)
