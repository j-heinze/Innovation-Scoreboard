import dash
import dash_table
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
                columns=[{"name": i, "id": i}
                         for i in ["Stand", "Anzahl Mitarbeiter", "Betriebsertrag/Jahr tsd. Euro", "Gewinn/Verlust vor Steuern tsd. EUR", "Gewinn pro Mitarbeiter tsd. EUR", "F&E Ausgaben tsd. EUR"]],
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
                         for i in ["Eigenkapital tsd. EUR", "Fremd- zu Eigenkapital (%)", "Eigenkapitalquote (%)", "ROE vor Steuern (%)", "ROCE vor Steuern (%)", "Langfristige Verbindlichkeiten tsd. EUR", "EBITDA tsd. EUR",  "Cashflow tsd. Euro"]],
                sort_action="none",
                sort_mode="single",
            )
            ], style={"width": "100%", "padding-left": "0.5rem",  "padding-right": "0.5rem", "padding-bottom": "3rem"})
         ]
    ),
    className="mt-3",
)
