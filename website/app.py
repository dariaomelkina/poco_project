import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from bitarray.util import ba2hex

from modules.simulator import CPU

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

with open("modules/program_examples/assembly_test4.bin", "r") as file:
    data = file.read()

cpu = CPU("risc3", "neumann", "special", data)


# def press_button():


def make_memory_slots():
    header_1 = []
    for i in range(0, 32, 4):
        header_1.append(
            " " + hex(i)[2:].rjust(2, "0") + " " + hex(i + 1)[2:].rjust(2, "0") + " " + hex(i + 2)[2:].rjust(2,
                                                                                                             "0") + " " + hex(
                i + 3)[2:].rjust(2, "0") + " |")
    header_1 = "".join(header_1)

    rows = []
    for i in range(0, 1024, 32):
        rows.append(hex(i)[2:].rjust(8, "0"))

    memory_data = []
    for i in range(0, len(cpu.data_memory.slots), 32 * 8):
        memory_data.append(ba2hex(cpu.data_memory.slots[i:i + 32 * 8]))

    fig = go.Figure(
        data=[go.Table(header=dict(values=["Addr       :  ", header_1]), cells=dict(values=[rows, memory_data]))])
    return fig


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div([
    html.Button('Next', id='submit-val', n_clicks=0, style={'display': 'inline-block'}),
    html.Div(id='simulator')
])


@app.callback(Output('simulator', 'children'),
              [Input('submit-val', 'n_clicks')])
def update_tables(n_clicks):
    cpu.web_next_instruction()
    return html.Div([
        html.Div(dcc.Graph(figure=make_memory_slots(), config={
        'displayModeBar': False})),
    ])


server = app.server
dev_server = app.run_server

# run the program
if __name__ == '__main__':
    app.run_server(debug=True)
    # app.run_server(debug=True, processes=3, threaded=False)

