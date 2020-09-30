import dash
import dash_table
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc


maininfo = dbc.Card(
    dbc.CardBody(
        [html.H5("Übersicht"), dash_table.DataTable(
            id='maininfo-table',
            style_cell={
                'height': 'auto',
                # all three widths are needed
                # 'maxWidth': '60px',
                'minWidth': '30px', 'width': '60px', 'maxWidth': '120px',
                'whiteSpace': 'normal',
                "text-align": "left"
            },
            columns=[{"name": i, "id": i}
                     for i in ["BvD ID Nummer", "Globale KM - Name", "Stand", "Anzahl Mitarbeiter", "Eigenkapitalquote (%)"]],
            sort_action="none",
            sort_mode="single",
        ), html.H5("Innovation Scoreboard"), html.P("Detaillierte Beschreibungen der einzelnen Indikatoren finden sich unter dem Tab Patentindikatoren. "),
            html.Div([
                html.Div(
                    [dcc.Graph(id='Innovationsniveau_main', style={"height": "24vh"})
                     ], className="pretty_container", style={"width": "50%", 'height': '26vh'}),

                html.Div([dcc.Graph(id='Innovationsfrequenz_main', style={"height": "24vh"})],
                         className="pretty_container", style={"width": "50%", 'height': '26vh'}
                         )], style={'width': '100%', 'display': 'flex'}),
            html.Div(
            [html.Div(
                [dcc.Graph(id='Innovationsfähigkeit_main', style={"height": "24vh"}
                           )], className="pretty_container", style={"width": "50%", 'height': '26vh'}
            ),
                html.Div(
                [dcc.Graph(id='Innovationscharakter_main', style={"height": "24vh"}
                           )], className="pretty_container", style={"width": "50%", 'height': '26vh'}
            ), ], style={"display": "flex", "width": "100%"}
        )
        ], className="mb-3"

    )
)
