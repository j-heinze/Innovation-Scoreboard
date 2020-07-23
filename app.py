import json

import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.express as px
import plotly.graph_objects as go

import pandas as pd

df = pd.read_pickle('MedizinInnovationsindex.pkl')
dfnumericnorm = pd.read_pickle('Medizinnormiertnumerics.pkl')
meandata = dfnumericnorm.mean()
qualitativ = pd.read_pickle('Medizinqualitativ.pkl')
kooperationen = pd.read_pickle("MedizinKooperationen.pkl")
Frequenz = pd.read_pickle("MedizinAnzahldict.pkl")
FrequenzIssue = pd.read_pickle("MedizinIssueAnzahldict.pkl")


app = dash.Dash(__name__, external_stylesheets=[
                dbc.themes.BOOTSTRAP])

server = app.server
available_indicators = list(df.columns)
df["company"] = df.index
dfnumericnorm["company"] = dfnumericnorm.index


app.layout = html.Div([html.Div([
    html.H1("Innovation Scoreboard"),
    html.Div([
        html.H6("Datensatz: Medizindatensatz"),
        html.P("Folgend das Filterkriterium auswählen und dimensionieren, um das XY-Diagramm zu filtern."),
        html.Div([

            dcc.Input(
                id='min-number',
                type='number',
                value=10,
                style={'width': '10%'}
            ),
            html.P("<", style={'width': '5%',
                               'display': 'flex', "justify-content": "center"}),
            dcc.Dropdown(
                id='Filterkriterium',
                options=[{'label': i, 'value': i}
                         for i in available_indicators],
                value='Anzahl Patente',
                style={'width': '100%'}
            ),
            html.P("<", style={'width': '5%',
                               'display': 'flex', "justify-content": "center"}),
            dcc.Input(
                id='max-number',
                type='number',
                value=400,
                style={'width': '10%'}
            )
        ], className="pretty_container", style={'width': '96%', 'display': 'flex', "items-align": "center"}),



    ]),
    html.Div(
        [dcc.Graph(id='graph'
                   ),
         html.P(
            "Hier auswählen, welche Indikatoren auf der Y und X-Achse abgebildet werden sollen:"),
         html.Div([
             html.Div([
                 dcc.Dropdown(
                     id='yaxis-column',
                     options=[{'label': i, 'value': i}
                              for i in available_indicators],
                     value='Zitationsrate'
                 ),
                 dcc.RadioItems(
                     id='yaxis-type',
                     options=[{'label': i, 'value': i}
                              for i in ['Linear', 'Log']],
                     value='Linear',
                     labelStyle={'display': 'inline-block'}
                 )
             ], style={'width': '40%'}),

             html.Div([
                 dcc.Dropdown(
                     id='xaxis-column',
                     options=[{'label': i, 'value': i}
                              for i in available_indicators],
                     value='Patentzitationsindex'
                 ),
                 dcc.RadioItems(
                     id='xaxis-type',
                     options=[{'label': i, 'value': i}
                              for i in ['Linear', 'Log']],
                     value='Linear',
                     labelStyle={'display': 'inline-block'}
                 )
             ],
                 style={'width': '40%'})
         ], style={'display': 'flex', "justify-content": "space-between", 'width': '100%'}),
         ], className="pretty_container", style={'width': '96%'},
    ),
    html.Div(
        [html.H3("Details: ", style={"padding-right": "2rem"}),
         html.H3(id='clickData')
         ], style={"display": "flex", "align-items": "center", "width": "96%"}),
    html.P("Nach der Auswahl eines Assignees im XY-Diagramm werden hier detaillierte Innovationsindikatoren angezeigt, die jeweils normiert sind und daher abweichen können."),
    html.Div([
        html.Div(
            [dcc.Graph(id='Innovationsfrequenz')], className="pretty_container", style={'width': '60%', 'display': 'inline-block'}),
        html.Div(
            [html.P(id='Median'),
             html.P(id='Mean'),
             html.P(id='Details'),
             html.P(id='AnzahlPatente')
             ],
            className="pretty_container", style={'width': '36%', 'display': 'inline-block'})], style={"display": "flex"}),
    html.Div([

        html.Div(
            [dcc.Graph(id='Innovationsniveau'
                       )], className="pretty_container", style={'width': '48%', 'display': 'inline-block'}
        ),
        html.Div(
            [dcc.Graph(id='CPC-Pie-Chart'
                       )], className="pretty_container", style={'width': '48%', 'display': 'inline-block'}
        )
    ], style={"display": "flex"}),
    html.Div([

        html.Div(
            [dcc.Graph(id='Innovationsfähigkeit'
                       )], className="pretty_container", style={'width': '48%', 'display': 'inline-block'}
        ),
        html.Div(
            [dcc.Graph(id='Innovationscharakter'
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
        [dcc.Graph(id='Innovationscharakter - Claims')
         ], className="pretty_container", style={'width': '48%', 'display': 'inline-block'}),
        html.Div(
        [dcc.Graph(id='KindCode-Pie-Chart')], className="pretty_container", style={'width': '48%', "padding": "0 8rem 10rem 0", 'display': 'inline-block'},
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

    ], style={"width": "90%"}),
    html.Div([html.H3("Kooperationen"), html.P("Daten können abweichen, da für die oben gezeigten Daten Assignees, die lediglich eine Kooperation haben und sonst nicht im Datensatz auftauchen entfernt wurden."), dash_table.DataTable(
        id='Kooperationen-table',
        style_cell={
            'whiteSpace': 'normal',
            'height': 'auto',
            "text-align": "left",
            'maxWidth': '180px'
        },
        columns=[{"name": i, "id": i} for i in kooperationen.columns],
        sort_action="native",
        sort_mode="single",
    )

    ])

], style={"width": "90%", "display": "block", "justify-content": "center"})], style={"width": "100%", "display": "flex", "justify-content": "center"})


@ app.callback(
    Output('graph', 'figure'),
    [Input('xaxis-column', 'value'),
     Input('yaxis-column', 'value'),
     Input('xaxis-type', 'value'),
     Input('yaxis-type', 'value'),
     Input('Filterkriterium', 'value'),
     Input('min-number', 'value'),
     Input('max-number', 'value')
     ])
def update_graph(xaxis_column_name, yaxis_column_name, xaxis_type, yaxis_type, Filterkriterium, min_number, max_number):

    # filterkriterium
    if min_number and max_number and Filterkriterium:
        if max_number > min_number:
            dataframefiltered = df[(df[Filterkriterium] > min_number) & (
                df[Filterkriterium] < max_number)]
        else:
            dataframefiltered = df
    else:
        dataframefiltered = df

    fig = px.scatter(dataframefiltered,
                     x=xaxis_column_name,
                     y=yaxis_column_name,
                     size='Anzahl Patente',
                     color='Anzahl Patente',
                     hover_name="company",
                     color_continuous_scale=px.colors.sequential.Viridis
                     )

    fig.update_layout(margin=dict(l=30, r=30, b=20, t=40), hovermode='closest',
                      plot_bgcolor="#F9F9F9", paper_bgcolor="#F9F9F9", font=dict(
        color="grey"
    ), hoverlabel=dict(

        font_size=14,
        font_family="Roboto"
    )
    )

    # fig.update_traces(marker=dict(color = "red"))
    fig.update_xaxes(title=xaxis_column_name,
                     type='linear' if xaxis_type == 'Linear' else 'log', gridcolor='lightgrey')

    fig.update_yaxes(title=yaxis_column_name,
                     type='linear' if yaxis_type == 'Linear' else 'log', gridcolor='lightgrey')
    return fig


@ app.callback(Output('clickData', 'children'),
               [Input('graph', 'clickData')])
def display_hover_data(clickData):
    if clickData:
        return clickData["points"][0]["hovertext"]


@ app.callback(Output('Innovationsfrequenz', 'figure'),
               [Input('graph', 'clickData')])
def update_Details_Innovationsfrequenz(clickData):
    if clickData:
        data = Frequenz[clickData["points"][0]["hovertext"]]
        dataIssue = FrequenzIssue[clickData["points"][0]["hovertext"]]

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=list(data.keys()),
            y=list(data.values()),
            name="Anzahl angemeldeter Patente im Jahr",
            marker_color='#7B2D41',
        ))
        fig.add_trace(go.Bar(
            x=list(dataIssue.keys()),
            y=list(dataIssue.values()),
            name="Anzahl erteilter Patente im Jahr",
            marker_color='#A0988C',
        ))
        fig.update_layout(margin=dict(l=30, r=30, b=20, t=40), hovermode='closest',
                          plot_bgcolor="#F9F9F9", paper_bgcolor="#F9F9F9", font=dict(
            color="grey"
        ), hoverlabel=dict(

            font_size=14,
            font_family="Roboto"
        ), legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.15,
            xanchor="right",
            x=1
        ),
            title='Innovationsfrequenz'
        )
        return fig
    return {}


@ app.callback(Output('AnzahlPatente', 'children'),
               [Input('graph', 'clickData')])
def get_AnzahlPatente(clickData):
    if clickData:
        return "Anzahl Patente im Datensatz: " + str(df.loc[clickData["points"][0]["hovertext"]]["Anzahl Patente"])


@ app.callback(Output('Mean', 'children'),
               [Input('graph', 'clickData')])
def get_mean(clickData):
    if clickData:
        return "Durchschnittliche Anmeldezeit: " + qualitativ.loc[clickData["points"][0]["hovertext"]]["Mean Application Time"].strftime("%m/%d/%Y")


@ app.callback(Output('Median', 'children'),
               [Input('graph', 'clickData')])
def get_median(clickData):
    if clickData:
        return "Durchschnittliche Erteilungszeit: " + qualitativ.loc[clickData["points"][0]["hovertext"]]["Mean Issue Time"].strftime("%m/%d/%Y")


@ app.callback(Output('Innovationsniveau', 'figure'),
               [Input('graph', 'clickData')])
def update_Details_Innovationsniveau(clickData):
    if clickData:
        DataSelect = dfnumericnorm[dfnumericnorm["company"]
                                   == clickData["points"][0]["hovertext"]]
        InnovationsniveauDF = DataSelect[["Anzahl Patente", "Zitationsrate", "Größte Zitationszahl",
                                          "Zitierhäufigkeit", "Patentzitationsindex", "hIndex", "Selbstzitationszahl"]]

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=list(InnovationsniveauDF.columns),
            y=[item for sublist in list(InnovationsniveauDF.values)
               for item in sublist],
            name=clickData["points"][0]["hovertext"],
            marker_color='#91C65D',

        ))

        fig.add_trace(go.Bar(
            x=["Anzahl Patente", "Zitationsrate", "Größte Zitationszahl",
                "Zitierhäufigkeit", "Patentzitationsindex", "hIndex", "Selbstzitationszahl"],
            y=meandata[["Anzahl Patente", "Zitationsrate", "Größte Zitationszahl",
                        "Zitierhäufigkeit", "Patentzitationsindex", "hIndex", "Selbstzitationszahl"]].values,
            name="Durchschnitt im Datensatz",
            marker_color='gainsboro',

        ))
        fig.update_layout(margin=dict(l=30, r=30, b=20, t=40), hovermode='closest',
                          plot_bgcolor="#F9F9F9", paper_bgcolor="#F9F9F9", font=dict(
            color="grey"
        ), hoverlabel=dict(

            font_size=14,
            font_family="Roboto"
        ), legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.5,
            xanchor="right",
            x=1
        ),
            title='Innovationsniveau'
        )

        return fig
    else:
        return {}


@ app.callback(Output('CPC-Pie-Chart', 'figure'),
               [Input('graph', 'clickData')])
def update_Details_CPC(clickData):
    if clickData:
        DataSelect = dfnumericnorm[dfnumericnorm["company"]
                                   == clickData["points"][0]["hovertext"]]
        InnovationspieDF = DataSelect[[
            "CPC - Refinement", "CPC - Combination", "CPC - Novel Combination", "CPC - Origination"]]

        fig = px.pie(InnovationspieDF,
                     values=[item for sublist in list(
                         InnovationspieDF.values) for item in sublist],
                     names=list(InnovationspieDF.columns),
                     title='CPC-Code Shares',
                     color_discrete_sequence=px.colors.sequential.Viridis)

        fig.update_layout(legend={'traceorder': 'normal'},
                          margin=dict(l=30, r=30, b=20, t=40), hovermode='closest',
                          plot_bgcolor="#F9F9F9", paper_bgcolor="#F9F9F9", font=dict(
            color="grey"
        ), hoverlabel=dict(

            font_size=14,
            font_family="Roboto"
        ),
            title='CPC-Code Shares'
        )

        return fig
    else:
        return {}


@ app.callback(Output('Innovationsfähigkeit', 'figure'),
               [Input('graph', 'clickData')])
def update_Details_Innovationsfähigkeit(clickData):
    if clickData:
        DataSelect = dfnumericnorm[dfnumericnorm["company"]
                                   == clickData["points"][0]["hovertext"]]
        InnovationsfähigkeitDF = DataSelect[["Anzahl individueller Erfinder", "Anzahl individueller Erfinder/Patente", "Intensität der Zusammenarbeit",
                                             "Durchschnittliche Anzahl Erfinder pro Patent (Teamgröße)", "Price Law Key Inventor Amount", "Real Key Inventor Amount", "Anzahl Kooperationen"]]

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=["individuelle Erfinder", "individuelle Erfinder/Patente", "Intensität der Zusammenarbeit",
                "Durchschnittliche Teamgröße", "Schlüsselerfinder (Price Law)", "Schlüsselerfinder (min. 3 Patente)", "Anzahl Kooperationen"],
            y=[item for sublist in list(InnovationsfähigkeitDF.values)
               for item in sublist],
            name=clickData["points"][0]["hovertext"],
            marker_color='#283A3E',
        ))
        fig.add_trace(go.Bar(
            x=["individuelle Erfinder", "individuelle Erfinder/Patente", "Intensität der Zusammenarbeit",
                "Durchschnittliche Teamgröße", "Schlüsselerfinder (Price Law)", "Schlüsselerfinder (min. 3 Patente)", "Anzahl Kooperationen"],
            y=meandata[["Anzahl individueller Erfinder", "Anzahl individueller Erfinder/Patente", "Intensität der Zusammenarbeit",
                        "Durchschnittliche Anzahl Erfinder pro Patent (Teamgröße)", "Price Law Key Inventor Amount", "Real Key Inventor Amount", "Anzahl Kooperationen"]].values,
            name="Durchschnitt im Datensatz",
            marker_color='gainsboro',
        ))

        fig.update_layout(margin=dict(l=30, r=30, b=20, t=40), hovermode='closest',
                          plot_bgcolor="#F9F9F9", paper_bgcolor="#F9F9F9", font=dict(
            color="grey"
        ), hoverlabel=dict(

            font_size=14,
            font_family="Roboto"
        ), legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.7,
            xanchor="right",
            x=1
        ),
            title='Innovationsfähigkeit'
        )

        return fig
    else:
        return {}


@ app.callback(Output('Innovationscharakter', 'figure'),
               [Input('graph', 'clickData')])
def update_Details_Innovationscharakter(clickData):
    if clickData:
        DataSelect = dfnumericnorm[dfnumericnorm["company"]
                                   == clickData["points"][0]["hovertext"]]
        InnovationscharakterDF = DataSelect[["Technologische Breite norm.",
                                             "TokenNovelty - Uniqueness", "Percentage Scientific Linkage", "Scientific Linkage Amount"]]

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=["Technologische Breite norm.",
               "TokenNovelty - Uniqueness", "Percentage Scientific Linkage", "Scientific Linkage Amount"],
            y=[item for sublist in list(InnovationscharakterDF.values)
               for item in sublist],
            name=clickData["points"][0]["hovertext"],
            marker_color='#21A7E9',
        ))

        fig.add_trace(go.Bar(
            x=["Technologische Breite norm.",
               "TokenNovelty - Uniqueness", "Percentage Scientific Linkage", "Scientific Linkage Amount"],
            y=meandata[["Technologische Breite norm.",
                        "TokenNovelty - Uniqueness", "Percentage Scientific Linkage", "Scientific Linkage Amount"]].values,
            name="Durchschnitt im Datensatz",
            marker_color='gainsboro',
        ))

        fig.update_layout(margin=dict(l=30, r=30, b=20, t=40), hovermode='closest',
                          plot_bgcolor="#F9F9F9", paper_bgcolor="#F9F9F9", font=dict(
            color="grey"
        ), hoverlabel=dict(

            font_size=14,
            font_family="Roboto"
        ), legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.7,
            xanchor="right",
            x=1
        ),
            title='Innovationscharakter'
        )

        return fig
    else:
        return {}


@ app.callback(Output('Innovationscharakter - Claims', 'figure'),
               [Input('graph', 'clickData')])
def update_Details_Innovationscharakter(clickData):
    if clickData:
        DataSelect = dfnumericnorm[dfnumericnorm["company"]
                                   == clickData["points"][0]["hovertext"]]
        InnovationscharakterDF = DataSelect[["Claim Length Value Index", "1st Claim length", "Claim Complexity Value Index",
                                             "Claim Complexity", "Claim Amount Value Index", "Claim Amount", "Claims Uniqueness"]]

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=["Claim Length Value Index", "1st Claim length", "Claim Complexity Value Index",
                "Claim Complexity", "Claim Amount Value Index", "Claim Amount", "Claims Uniqueness"],
            y=[item for sublist in list(InnovationscharakterDF.values)
               for item in sublist],
            name=clickData["points"][0]["hovertext"],
            marker_color='#21A7E9',
        ))

        fig.add_trace(go.Bar(
            x=["Claim Length Value Index", "1st Claim length", "Claim Complexity Value Index",
                "Claim Complexity", "Claim Amount Value Index", "Claim Amount", "Claims Uniqueness"],
            y=meandata[["Claim Length Value Index", "1st Claim length", "Claim Complexity Value Index",
                        "Claim Complexity", "Claim Amount Value Index", "Claim Amount", "Claims Uniqueness"]].values,
            name="Durchschnitt im Datensatz",
            marker_color='gainsboro',
        ))

        fig.update_layout(margin=dict(l=30, r=30, b=20, t=40), hovermode='closest',
                          plot_bgcolor="#F9F9F9", paper_bgcolor="#F9F9F9", font=dict(
            color="grey"
        ), hoverlabel=dict(

            font_size=14,
            font_family="Roboto"
        ), legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.5,
            xanchor="right",
            x=1
        ),
            title='Innovationscharakter - Claims'
        )

        return fig
    else:
        return {}


@ app.callback(Output('KindCode-Pie-Chart', 'figure'),
               [Input('graph', 'clickData')])
def update_Details_CPC(clickData):
    if clickData:
        DataSelect = dfnumericnorm[dfnumericnorm["company"]
                                   == clickData["points"][0]["hovertext"]]
        InnovationspieDF = DataSelect[[
            "B1 - Anteil", "B2 - Anteil", "A - Anteil", "C1 - Anteil"]]

        fig = px.pie(InnovationspieDF,
                     values=[item for sublist in list(
                         InnovationspieDF.values) for item in sublist],
                     names=list(InnovationspieDF.columns),
                     title='KindCode Shares',
                     color_discrete_sequence=px.colors.sequential.Viridis)

        fig.update_layout(legend={'traceorder': 'normal'},
                          margin=dict(l=30, r=30, b=20, t=40), hovermode='closest',
                          plot_bgcolor="#F9F9F9", paper_bgcolor="#F9F9F9", font=dict(
            color="grey"
        ), hoverlabel=dict(

            font_size=14,
            font_family="Roboto"
        ),
            title='KindCode Shares'
        )

        return fig
    else:
        return {}


@ app.callback(Output('Kooperationen-table', 'data'),
               [Input('graph', 'clickData')])
def update_table(clickData):
    if clickData:
        if clickData["points"][0]["hovertext"] in kooperationen.index:
            data = kooperationen.loc[[clickData["points"][0]["hovertext"]]]
            return data.to_dict('records')
        else:
            return [{"Partner": "Keine Partner", "Patente": "Keine Kooperationen im Datensatz", "Anzahl Kooperationen": 0}]
    else:
        return [{"Partner": "Keine Partner", "Patente": "Keine Kooperationen im Datensatz", "Anzahl Kooperationen": 0}]


@ app.callback(
    Output("modal", "is_open"),
    [Input("open", "n_clicks"), Input("close", "n_clicks")],
    [State("modal", "is_open")],


)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


@ app.callback(Output('Details', 'children'),
               [Input('graph', 'clickData')])
def display_hover_data(clickData):
    if clickData:
        keyinventors = qualitativ.loc[clickData["points"]
                                      [0]["hovertext"]]["Key Inventor Names"]
        if type(keyinventors) == list:
            return "Schlüsselerfinder: " + " ".join(keyinventors)
        else:
            return "Nicht genügend Daten über Erfinder vorhanden."


@ app.callback(Output('DetailsUniqueTerms', 'children'),
               [Input('graph', 'clickData')])
def display_hover_data(clickData):
    if clickData:
        return " Top 30 Unique Terms: " + ", ".join(qualitativ.loc[clickData["points"][0]["hovertext"]]["Uniqueterms Walther"][:30])


@ app.callback(Output('CPC-table', 'data'),
               [Input('graph', 'clickData')])
def update_table(clickData):

    if clickData:
        if clickData["points"][0]["hovertext"] in qualitativ[["Codestext"]].index:
            data = qualitativ[["Codestext"]].loc[[
                clickData["points"][0]["hovertext"]]]
            data = data.explode("Codestext")
            data["Code"] = data["Codestext"].apply(lambda x: x[0])
            data["Beschreibung"] = data["Codestext"].apply(
                lambda x: x[1])
            data["Auftreten in Patenten"] = data["Codestext"].apply(
                lambda x: x[2])
            data.drop("Codestext", axis=1, inplace=True)
            return data.to_dict('records')
        else:
            return [{"Code": "Keine Codes", "Beschreibung": "Keine Daten vorhanden", "Auftreten in Patenten": "Keine Daten vorhanden"}]
    else:
        return [{"Code": "Keine Codes", "Beschreibung": "Keine Daten vorhanden", "Auftreten in Patenten": 0}]


if __name__ == '__main__':
    app.run_server(host="0.0.0.0", debug=True)
