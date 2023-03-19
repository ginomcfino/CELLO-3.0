from dash import Dash, dcc, html, Input, Output
from dash.exceptions import PreventUpdate
import json
import os
import glob
import requests

# TODO: Correctly link all of the ucf files and their names
# TODO: Also be able to link schemas the schemas folder
# TODO: Make this save_path route to AWS storage
retrieval_url = 'https://github.com/CIDARLAB/Cello-UCF/develop/files/v2/<input/output/ucf>/<filename>'

# save_path = '/path/to/save/file/<filename>'
# response = requests.get(retrieval_url)
# if response.status_code == 200:
#     with open(save_path, 'wb') as f:
#         f.write(response.content)
#     print('File downloaded successfully.')
# else:
#     print('Failed to download file.')


# TODO: Implement AWS S3 to host UCF Files
# TODO: Retrieve UCF files with REST API
# TODO: Implement AWS ElastiCache for in-memory storage
ucf_path = '../../IO/inputs'
cur_dir = os.getcwd()
os.chdir(ucf_path)
extension = '.json'
ucf_files = sorted(list(glob.glob('*' + extension)))
os.chdir(cur_dir)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(
    children=[
        # Data Storage in Local Meomory
        # dcc.Store(id='ucf-data', storage_type='local'),

        # html components
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
                html.Div(children=[
                    html.Label('Select UCF template: '),
                    dcc.Dropdown(ucf_files, ucf_files[0], id='ucf_select'),

                    html.Br(),
                ], style={'padding': 10,
                          'flex': 1,
                          'padding-left': '100px',
                          'padding-right': '100px'
                          }
                ),
            ],
            style={
                'textAlign': 'center',
                'display': 'flex',
                'flex-direction': 'row'
            }
        ),

        html.Div([
            html.H5('UCF preview: '),
            html.Div(id='ucf_preview', style={
                'padding-left': '100px',
                'padding-right': '100px'
            }),
            html.Br(),
            html.Div([
                "Please select a collection to modify: ",
                dcc.Input(id='ucf_choice', value='-----', type='text'),
                html.Button(id='pick_ucf_button',
                            n_clicks=0, children='Submit')
            ],
            ),
            html.Br(),
            # html.P(id='ucf_collection_names')
        ],
            style={
                'text-align': 'center',
        }
        ),


    ],
    style={
        'display': 'flex',
        'flex-direction': 'column',
    }
)

# @app.callback(
#     Output('ucf-data', 'data'),
#     Input('ucf_select', 'value')
# )
# def select_ucf(ucf_name):
#     with open(os.path.join(ucf_path, ucf_name), 'r') as f:
#         ucf_data = json.load(f)
#         print('\'Click\'')
#         print(json.dumps(ucf_data[0], indent=4))
#         print()
#         print()
#     return ucf_data


@app.callback(
    Output('ucf_preview', 'children'),
    Input('ucf_select', 'value')
)
def select_ucf(ucf_name):
    with open(os.path.join(ucf_path, ucf_name), 'r') as f:
        ucf_data = json.load(f)
        print('\'Click\'')
        print(json.dumps(ucf_data[0], indent=4))
        print()
        print()
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


# @app.callback(
#     Output('ucf_preview', 'children'),
#     Input('ucf-data', 'data')
# )
# def this_function_name_does_not_even_matter(ucf):
#     if ucf is None:
#         raise PreventUpdate
#     return html.Div(
#         html.Pre(json.dumps(ucf[:10], indent=4)),
#         style={
#             'height': '500px',
#             'overflow': 'auto',
#             'white-space': 'nowrap',
#             'background-color': 'rgba(128, 128, 128, 0.1)',
#             'text-align': 'left'
#         }
#     )

# @app.callback(
#     Output('ucf_collection_names', 'children'),
#     Input('ucf_preview', 'children')
# )
# def get_ucf_collection_names(ucf):
#     if ucf is None:
#         print("ERROR")
#         raise PreventUpdate
#     collections = []
#     for i in ucf:
#         collections.append(i['collection'])
#     return collections + ' what is this? '


if __name__ == '__main__':
    app.run_server(debug=True)
