import dash
import dash_table
from dash_table.Format import Format, Scheme
import dash_bootstrap_components as dbc
import dash_html_components as html


finance = dbc.Card(
    dbc.CardBody(
        [html.H4("Übersicht", style={"width": "100%"}),
            html.Div(
            [dash_table.DataTable(
                id='finance-table-overview',
                style_cell={
                    'height': 'auto',
                    # all three widths are needed
                    # 'maxWidth': '60px',
                    'minWidth': '30px', 'width': '60px', 'maxWidth': '120px',
                    'whiteSpace': 'normal',
                    "text-align": "left"
                },
                columns=[{"name": "Stand", "id": "Stand"}, {"name": "Anzahl Mitarbeiter", "id": "Anzahl Mitarbeiter"},
                         {"name": "Betriebsertrag/Jahr tsd. Euro", "id": "Betriebsertrag/Jahr tsd. Euro", "type": "numeric", "format": Format(precision=2, scheme=Scheme.fixed)}, {
                             "name": "Gewinn/Verlust vor Steuern tsd. EUR", "id": "Gewinn/Verlust vor Steuern tsd. EUR", "type": "numeric", "format": Format(precision=2, scheme=Scheme.fixed)}, {"name": "F&E Ausgaben tsd. EUR", "id": "F&E Ausgaben tsd. EUR", "type": "numeric", "format": Format(precision=2, scheme=Scheme.fixed)}],
                sort_action="none",
                sort_mode="single",
            )
            ], style={"width": "100%", "padding-left": "0.5rem", "padding-right": "0.5rem", "padding-bottom": "1rem"}),
            html.H4("Eigenkapitalinformation", style={"width": "100%"}),
            html.Div(
            [dash_table.DataTable(
                id='finance-table-eigenkapital',
                style_cell={
                    'height': 'auto',
                    # all three widths are needed
                    'minWidth': '30px', 'width': '60px', 'maxWidth': '120px',
                    'whiteSpace': 'normal',
                    "text-align": "left"
                },
                columns=[{"name": i, "id": i}
                         for i in ["Eigenkapital tsd. EUR", "Eigenkapitalquote (%)", "ROE vor Steuern (%)" "ROA vor Steuern (%)", "ROCE vor Steuern (%)", "ROS nach Steuern(%)", "Langfristige Verbindlichkeiten tsd. EUR", "EBITDA tsd. EUR"]],
                sort_action="none",
                sort_mode="single",
            )
            ], style={"width": "100%", "padding-left": "0.5rem",  "padding-right": "0.5rem", "padding-bottom": "3rem"})
         ]
    ),
    className="mt-3",
)
