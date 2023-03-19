from dash import Dash, dcc, html
from datetime import date

app = Dash(__name__)

app.layout = html.Div([
    dcc.DatePickerRange(
        id='date-picker-range',
        start_date_placeholder_text='Select a! date!',
        end_date_placeholder_text='Select! a date!'
    ),
    ],
    style={
        'text-align' : 'center',
    }
)

if __name__ == '__main__':
    app.run_server(debug=True)