from dash import Dash, dcc, html, Input, Output
from dash.exceptions import PreventUpdate
import json
import requests

# TODO: Correctly link all of the ucf files and their names
# TODO: Also be able to link schemas the schemas folder
# TODO: Make this save_path route to AWS storage

# Making requests is OK because this is a public repo
UCFs_folder = 'https://raw.githubusercontent.com/ginomcfino/CELLO-3.0/dev-merge/UCFormatter/UCFs'
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


# TODO: Implement AWS S3 to host UCF Files
# TODO: Retrieve UCF files with REST API
# TODO: Implement AWS ElastiCache for in-memory storage


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
                html.Div(children=[
                    html.Label('Select UCF template: '),
                    dcc.Dropdown(ucf_list, ucf_list[0], id='ucf_select'),

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
            html.P(id='ucf_collection_names')
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


@app.callback(
    Output('ucf_preview', 'children'),
    Input('ucf_select', 'value')
)
def select_ucf(ucf_name):    
    with requests.get(UCFs_folder+'/'+ucf_name) as response:
        if response.ok:
            ucf_data = json.loads(response.content)
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
    

if __name__ == '__main__':
    app.run_server(debug=True)
