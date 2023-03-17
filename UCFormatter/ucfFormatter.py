from dash import Dash, dcc, html, Input, Output
import json
import os
import glob
import copy

ucf_path = '../../IO/inputs'
cur_dir = os.getcwd()
os.chdir(ucf_path)
extension = '.json'
ucf_files = sorted(list(glob.glob('*' + extension)))
os.chdir(cur_dir)
input_str = '< Select an UCF file to work on >\n'
for i in range(len(ucf_files)):
    if i < 10:
        line = f' {i}: {ucf_files[i]} \n'
    else:
        line = f'{i}: {ucf_files[i]} \n'
    input_str += line
choice = int(input(input_str))

# this is UCF file you are working on:
openUCF = ''
if choice in range(len(ucf_files)):
    openUCF = ucf_files[choice]
else:
    openUCF = 'Eco1C1G1T1.UCF.json' # default, should be a empty template instead
print("your chosen UCF: " + str(openUCF))
file_path = os.path.join(ucf_path, openUCF)
with open(file_path, 'r') as f:
    ucf = json.load(f)
# TODO Save the UCF as it's own class, 
# TODO Put this entire section in a Callback method
print(json.dumps(ucf[0], indent=4)) 

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(
    children=[
        html.H1(
            children='CELLO-V3',
            style={
                'textAlign': 'center',
                'color': '#111111',
                'flex' : 1,
                'backgroundColor' : 'grey',
                'height' : 'max-height',
            }
        ),
        html.H5(
            '''UCFormatter Tool''',
            style={'flex': 1, 'textAlign': 'center',},
        ),
        html.Br(),

        html.Div(
            children=[
                html.Div(style={'flex': 0.2, 'textAlign': 'center'}),
                html.Div(
                    '''
                    The Cello software designs the DNA sequences for programmable circuits 
                    based on a high-level software description and a library of characterized 
                    DNA parts representing Boolean logic gates.''',
                    style={'flex': 0.6, 'textAlign': 'center'},
                ),
                html.Div(style={'flex': 0.2, 'textAlign': 'center'}),
            ],
            style={
                'display': 'flex', 
                'flex-direction': 'row',
            }
        ),
        html.Div(
            children=[
                html.Div(style={'flex': 0.2, 'textAlign': 'center'}),
                html.Div(
                    '''
                    The user constraints file (UCF) is
                    a JavaScript Object Notation (JSON) file that describes 
                    a part and gate library for a particular organism.''',
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
            children= [
                html.Div(children=[
                    html.Label('Dropdown'),
                    dcc.Dropdown(['New York City', 'Montréal', 'San Francisco'], 'Montréal'),

                    html.Br(),
                    html.Label('Multi-Select Dropdown'),
                    dcc.Dropdown(['New York City', 'Montréal', 'San Francisco'],
                                ['Montréal', 'San Francisco'],
                                multi=True),

                    html.Br(),
                    html.Label('Radio Items'),
                    dcc.RadioItems(['New York City', 'Montréal', 'San Francisco'], 'Montréal'),
                ], style={'padding': 10, 'flex': 1}),

                html.Div(children=[
                    html.Label('Checkboxes'),
                    dcc.Checklist(['New York City', 'Montréal', 'San Francisco'],
                                ['Montréal', 'San Francisco']
                    ),

                    html.Br(),
                    html.Label('Text Input'),
                    dcc.Input(value='MTL', type='text'),

                    html.Br(),
                    html.Label('Slider'),
                    dcc.Slider(
                        min=0,
                        max=9,
                        marks={i: f'Label {i}' if i == 1 else str(i) for i in range(1, 6)},
                        value=5,
                    ),
                ], style={'padding': 10, 'flex': 1})
            ]
            , 
            style={
                'textAlign': 'center',
                'color': '#444444',
                'display': 'flex',
                'flex-direction': 'row'
            }
        ),

        html.Div([
            "Search for keyword: ",
            dcc.Input(id='my-input', value='-----', type='text')
        ]),
    ], 
    style={
        'display': 'flex', 
        'flex-direction': 'column',
    }
)


if __name__ == '__main__':
    app.run_server(debug=True)
