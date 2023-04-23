from dash import Dash, dcc, html, Input, Output, State, ctx
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import json
import subprocess
import uuid


def debug_print(msg):
    print(f'\nDEBUG: {msg}\n')
    
redis_server_process = None

def start_redis_server():
    global redis_server_process

    cmd = ['redis-cli', 'ping']
    try:
        subprocess.check_output(cmd)
        print('Redis server is already running.')
        return
    except subprocess.CalledProcessError:
        pass

    # Start Redis server
    cmd = ['redis-server']
    redis_server_process = subprocess.Popen(cmd)
    print('Redis server started.')

def stop_redis_server():
    global redis_server_process

    if redis_server_process:
        redis_server_process.terminate()
        redis_server_process.wait()
        print('Redis server stopped.')
        
def slider_helper(slider_value):
    if abs(slider_value[1] - slider_value[0]) != 10:
        if slider_value[1] > slider_value[0]:
            new_value = [slider_value[1] - 10, slider_value[1]]
        else:
            new_value = [slider_value[0], slider_value[0] + 10]
        slider_value = new_value
    return slider_value

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
    
def generate_schema_preview(schema=None):
    if schema is None:
        return html.Div(
            'select a collection name to preview',
            style={
                'height': '500px',
                'overflow': 'auto',
                'white-space': 'nowrap',
                'background-color': 'rgba(128, 128, 128, 0.1)',
                'display': 'flex',
                'align-items': 'center',
                'justify-content': 'center',
            }
        )
    else:
        return html.Div(
            html.Pre(json.dumps(schema, indent=4)),
            style={
                'height': '500px',
                'overflow': 'auto',
                'background-color': 'rgba(128, 128, 128, 0.1)',
                'text-align': 'left'
            }
        )
        
def find_collection_in_ucf(c_name, ucf):
    output = []
    for c in ucf:
        if c['collection'] == c_name:
            output.append(c)
    return output
    
def generate_input_components(data, level=0):
    input_components = []
    for key, value in data.items():
        if isinstance(value, dict):
            input_components.append(html.H5(key, style={'marginLeft': f"{level}em"}))
            input_components.extend(generate_input_components(value, level=level+1))
        elif isinstance(value, list):
            input_components.append(html.H5(key, style={'marginLeft': f"{level}em"}))
            for item in value:
                if isinstance(item, dict) or isinstance(item, list):
                    input_components.extend(generate_input_components(item, level=level+1))
        else:
            input_components.append(html.Div([
                html.Label(key, style={'marginLeft': f"{level+1}em"}),
                html.Br(),
                dcc.Input(
                    id={'type': 'input', 'level': level, 'key': key, 'id': str(uuid.uuid4())},
                    type='text',
                    value=value,
                    style={'marginLeft': f"{level+1}em"}
                ),
                html.Br()
            ]))
    return input_components