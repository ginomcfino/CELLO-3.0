from dash import Dash, dcc, html, Input, Output, State, ctx
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import json
import subprocess


def debug_print(msg):
    print(f'\nDEBUG: {msg}\n')

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
    