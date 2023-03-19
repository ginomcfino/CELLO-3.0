from dash import Dash, dcc, html, Input, Output
import json
import os
import glob

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
                    # html.Label('Multi-Select Dropdown'),
                    # dcc.Dropdown(['New York City', 'Montréal', 'San Francisco'],
                    #              ['Montréal', 'San Francisco'],
                    #              multi=True),

                    # html.Br(),
                    # html.Label('Radio Items'),
                    # dcc.RadioItems(['New York City', 'Montréal',
                    #                'San Francisco'], 'Montréal'),
                ], style={'padding': 10, 'flex': 1}),

                # html.Div(children=[
                #     html.Label('Checkboxes'),
                #     dcc.Checklist(['New York City', 'Montréal', 'San Francisco'],
                #                 ['Montréal', 'San Francisco']
                #     ),

                #     html.Br(),
                #     html.Label('Text Input'),
                #     dcc.Input(value='MTL', type='text'),

                #     html.Br(),
                #     html.Label('Slider'),
                #     dcc.Slider(
                #         min=0,
                #         max=9,
                #         marks={i: f'Label {i}' if i == 1 else str(i) for i in range(1, 6)},
                #         value=5,
                #     ),
                # ], style={'padding': 10, 'flex': 1})
            ],
            style={
                'textAlign': 'center',
                'display': 'flex',
                'flex-direction': 'row'
            }
        ),

        html.Div([
            html.H5('UCF preview: '),
            html.Div(id='ucf_name', style={
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
        ],
            style={
                'text-align': 'center',
        }
        ),

        # html.Div(
        #     children=[
        #         html.Div(style={'flex': 0.2, 'textAlign': 'center'}),
        #         html.Div(id='ucf_name', style={'flex': 0.6, 'textAlign': 'center'}),
        #         html.Div(style={'flex': 0.2, 'textAlign': 'center'}),
        #     ],
        #     style={
        #         'display': 'flex',
        #         'flex-direction': 'row',
        #     }
        # ),



    ],
    style={
        'display': 'flex',
        'flex-direction': 'column',
    }
)


@app.callback(
    Output('ucf_name', 'children'),
    Input('ucf_select', 'value')
)
def this_function_name_does_not_even_matter(ucf_name):
    with open(os.path.join(ucf_path, ucf_name), 'r') as f:
        ucf_json = json.load(f)
        print('\'Click\'')
        print(json.dumps(ucf_json[0], indent=4))
        print()
        print()
    return html.Div(
        html.Pre(json.dumps(ucf_json[:10], indent=2)),
        style={
            'height': '500px',
            'overflow': 'auto',
            'white-space': 'pre-wrap',
            'background-color': 'rgba(128, 128, 128, 0.1)'
        }
    )


if __name__ == '__main__':
    app.run_server(debug=True)
