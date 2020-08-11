import dash
import dash_table
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc


analytics = dbc.Card(
    dbc.CardBody(
        [
            html.Div([
                html.Div(
                    [dcc.Graph(id='Innovationsfrequenz', style={"height": "30vh"})], className="pretty_container", style={'width': '60%', 'display': 'inline-block'}),
                html.Div(
                    [html.P(id='Median'),
                     html.P(id='Mean'),
                        html.P(id='Details'),
                        html.P(id='AnzahlPatente')
                     ],
                    className="pretty_container", style={'width': '36%', 'display': 'inline-block'})], style={"display": "flex"}),
            html.Div([

                html.Div(
                    [dcc.Graph(id='Innovationsniveau', style={"height": "30vh"}
                               )], className="pretty_container", style={'width': '48%', 'display': 'inline-block'}
                ),
                html.Div(
                    [dcc.Graph(id='CPC-Pie-Chart', style={"height": "30vh"}
                               )], className="pretty_container", style={'width': '48%', 'display': 'inline-block'}
                )
            ], style={"display": "flex"}),
            html.Div([

                html.Div(
                    [dcc.Graph(id='Innovationsfähigkeit', style={"height": "30vh"}
                               )], className="pretty_container", style={'width': '48%', 'display': 'inline-block'}
                ),
                html.Div(
                    [dcc.Graph(id='Innovationscharakter', style={"height": "30vh"}
                               ), html.Div(
                        [
                            dbc.Button("Information", id="open"),
                            dbc.Modal(
                                [
                                    dbc.ModalHeader("Innovationscharakter"),
                                    dbc.ModalBody(dcc.Markdown('''
                    Qualitative Eigenschaften von Unternehmensinnovationen

                    **Technologische Breite**
                    Anzahl verschiedener CPC-Codes mit dem gleichen Assignee. (normiert über den Datensatz)
                    Bildet die technologische Breite des Patentportfolios des Assignees im Datensatz ab.

                    **1st Claim length**
                    Durchschnittliche Länge des ersten Claims normiert über den Datensatz. (normiert über den Datensatz)

                    **Claim Language**
                    Verhältnis der Länge des ersten Claims im Patent zu der Länge des ersten Claims eines ähnlichen Patents. Ähnlichkeitsmessung über Doc2Vec.

                    **TokenNovelty - Uniqueness**
                    Ähnlich zu CPC Novelty, wird zeitlich sortiert durch den Datensatz iteriert. Nur Skipgramme, die noch nicht im Datensatz vorhanden sind werden abgebildet.

                    Eigener Indikator:
                    Neue Skipgramme/ Gesamtzahl Skipgramme >=0.5 -> *Origination*
                    Neue Skipgramme/ Gesamtzahl Skipgramme >= 0.25 -> *Novel Combination*
                    Neue Skipgramme/ Gesamtzahl Skipgramme >=0.05 -> *Combination*
                    Neue Skipgramme/ Gesamtzahl Skipgramme <0.05 -> *Refinement*

                    **Claims Uniqueness**

                    **Percentage Scientific Linkage**

                    **Scientific Linkage Amount**

                    ''')),
                                    dbc.ModalFooter(
                                        dbc.Button("Close", id="close",
                                                   className="ml-auto")
                                    ),
                                ],
                                id="modal",
                                centered=True,
                                size="lg",
                                scrollable=True
                            ),
                        ]
                    )], className="pretty_container", style={'width': '48%', 'display': 'inline-block'}
                )
            ], style={"display": "flex"}),

            html.Div([html.Div(
                [dcc.Graph(id='Innovationscharakter - Claims', style={"height": "30vh"})
                 ], className="pretty_container", style={'width': '48%', 'display': 'inline-block'}),
                html.Div(
                [dcc.Graph(id='KindCode-Pie-Chart', style={"height": "30vh"})], className="pretty_container", style={'width': '48%', 'display': 'inline-block'},
            )
            ], style={"display": "flex"}),

            html.Div([html.H3("Qualitative Daten"), html.P(
                id='DetailsUniqueTerms')], style={"display": "block"}),

            html.Div([html.H3("CPC-Daten"), html.P("Die Subklassen der folgend aufgeführten CPC-Codes wurden ebenfalls mitgezählt. Es wird die Quadratwurzel der Anzahl der individuellen gekürzten CPC Codes pro Assignee als Anzahl verwendet."), dash_table.DataTable(
                id='CPC-table',
                style_cell={
                    'overflow': 'hidden',
                    'textOverflow': 'ellipsis',
                    'maxWidth': "65vw",
                },
                columns=[{"name": i, "id": i} for i in [
                    "Code", "Beschreibung", "Auftreten in Patenten"]],
                sort_action="native",
                sort_mode="single",
            )

            ], style={"width": "90%", "padding-left": "2rem"}),
            html.Div([html.H3("Kooperationen"), html.P("Daten können abweichen, da für die oben gezeigten Daten Assignees, die lediglich eine Kooperation haben und sonst nicht im Datensatz auftauchen entfernt wurden."), dash_table.DataTable(
                id='Kooperationen-table',
                style_cell={
                    'whiteSpace': 'normal',
                    'height': 'auto',
                    "text-align": "left",
                    'maxWidth': '65vw'
                },
                columns=[{"name": i, "id": i}
                         for i in ["Partner", "Patente", "Anzahl Kooperationen"]],
                sort_action="native",
                sort_mode="single",
            )

            ], style={"width": "90%", "padding-left": "2rem"})
        ]
    ),
    className="mt-3",
)
