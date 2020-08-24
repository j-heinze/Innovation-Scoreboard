import dash
import dash_table
import dash_core_components as dcc

from dash.dependencies import Input, Output, State
import plotly.express as px
import plotly.graph_objects as go

import dash_html_components as html
import dash_bootstrap_components as dbc

import numpy as np
import pandas as pd
import json
from tab_finance import finance
from tab_maininfo import maininfo
from tab_ip_analytics import analytics

Dataset = {}
for Datensatz in ["Medizin", "UVLED"]:
    df = pd.read_pickle(Datensatz + 'Innovationsindex.pkl')
    df["company"] = df.index
    available_indicators = list(df.columns)

    dfnumericnorm = pd.read_pickle(Datensatz + 'normiertnumerics.pkl')
    dfnumericnorm["company"] = dfnumericnorm.index
    meandata = dfnumericnorm.mean()
    qualitativ = pd.read_pickle(Datensatz + 'qualitativ.pkl')
    kooperationen = pd.read_pickle(Datensatz + "Kooperationen.pkl")
    Frequenz = pd.read_pickle(Datensatz + "Anzahldict.pkl")
    FrequenzIssue = pd.read_pickle(Datensatz + "IssueAnzahldict.pkl")
    Finanzdaten = pd.read_pickle("Finanzdaten_" + Datensatz + ".pkl")
    meanfinance = Finanzdaten.mean()
    Dataset[Datensatz] = {"df": df, "dfnumericnorm": dfnumericnorm, "meandata": meandata, "qualitativ": qualitativ,
                          "kooperationen": kooperationen, "Frequenz": Frequenz, "FrequenzIssue": FrequenzIssue, "Finanzdaten": Finanzdaten, "Finandatenmean": meanfinance}

app = dash.Dash(__name__, external_stylesheets=[
                dbc.themes.BOOTSTRAP])

server = app.server


app.layout = html.Div([
    html.Div([
        html.Div([html.H2("Innovation Scoreboard", style={"padding-right": "2rem"}),
                  dbc.Button("Datensatz wechseln",
                             id="mainopen", color="info"),
                  dbc.Modal(
            [
                dbc.ModalHeader("Datensatzauswahl"),
                dbc.ModalBody(html.Div([html.P("In diesem Projekt wurden zwei Datensätze untersucht:"),
                                        dbc.Card(dcc.Markdown('''**Personalisierte Medizin**  
                                        Patienten unter Einbeziehung individueller Gegebenheiten über funktionale Krankheitsdiagnose hinaus behandeln z.B. individuell optimale Medikamentenkombination zusammenstellen  
                                        Zwei Hauptbereiche  
                                        - Stoffschutz von Arzneimitteln  
                                        - Patentierungsmöglichkeiten in der Diagnostik'''), body=True),
                                        dbc.Card(dcc.Markdown('''**UV-LED**  
                                        UV-LED beschreibt eine Technologie mit einem breitem Anwendungsspektrum: Sie findet Anwendung im medizinischen, industriellen und persönlichen Gebrauch und zeichnet sich durch eine kontinuierliche Aktivität bei Patentierungen aus. Ein heute aktueller Anwendungsfall ist die Anwendung zur Desinfektion gegen SARS-CoV-2'''), body=True),
                                        html.H6("Datensatz: "),
                                        dcc.Dropdown(
                    id='Datensatz',
                    options=[{'label': "Personalisierte Medizin", 'value': "Medizin", "title": "Patienten unter Einbeziehung individueller Gegebenheiten über funktionale Krankheitsdiagnose hinaus behandeln"}, {
                        'label': "UV-LED", 'value': "UVLED", "title": "Anwendung im medizinischen, industriellen und persönlichen Gebrauch"}],
                    value='UVLED',
                    style={'width': '100%', "padding": "0 0 0 2rem"},
                    clearable=False,
                ), ], style={"display": "block", "align-items": "center"}),),
                dbc.ModalFooter(
                    dbc.Button("Auswahl bestätigen.",
                               id="close-lg", color="info", className="ml-auto")
                ),
            ],
            is_open=True,
            id="modalmain",
            size="lg",
            centered=True,
        )], style={"display": "flex", "align-items": "center"}),
        html.Div([
            html.P(
                "Folgend das Filterkriterium auswählen und dimensionieren, um das XY-Diagramm zu filtern."),
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
             html.H3("Bitte einen Anmelder im Diagramm oben auswählen.",
                     id='clickData')
             ], style={"display": "flex", "align-items": "center", "width": "96%"}),
        html.P("Nach der Auswahl eines Assignees im XY-Diagramm werden hier detaillierte Innovationsindikatoren angezeigt, die jeweils normiert sind und daher von den oben gezeigten Werten abweichen können."),
        dbc.Tabs(
            [
                dbc.Tab(maininfo, label="Zusammenfassung"),
                dbc.Tab(finance, label="Finanzdaten"),
                dbc.Tab(
                    analytics, label="Patentanalyse"
                ),
            ]
        )

    ], style={"width": "100%", "padding-left": "1rem", "display": "block", "justify-content": "center"})], style={"width": "100%", "justify-content": "center"})


@ app.callback(
    Output("modalmain", "is_open"),
    [Input("mainopen", "n_clicks"), Input("close-lg", "n_clicks")],
    [State("modalmain", "is_open")],

)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


@ app.callback(
    Output('graph', 'figure'),
    [Input('xaxis-column', 'value'),
     Input('yaxis-column', 'value'),
     Input('xaxis-type', 'value'),
     Input('yaxis-type', 'value'),
     Input('Filterkriterium', 'value'),
     Input('min-number', 'value'),
     Input('max-number', 'value'),
     Input("Datensatz", "value")
     ])
def update_graph(xaxis_column_name, yaxis_column_name, xaxis_type, yaxis_type, Filterkriterium, min_number, max_number, Datensatz):
    # filterkriterium
    if min_number and max_number and Filterkriterium:
        if max_number > min_number:
            dataframefiltered = Dataset[Datensatz]["df"][(Dataset[Datensatz]["df"][Filterkriterium] > min_number) & (
                Dataset[Datensatz]["df"][Filterkriterium] < max_number)]
        else:
            dataframefiltered = Dataset[Datensatz]["df"]
    else:
        dataframefiltered = Dataset[Datensatz]["df"]

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
               [Input('graph', 'clickData'), Input("Datensatz", "value")])
def display_hover_data(clickData, Datensatz):
    if clickData:
        if clickData["points"][0]["hovertext"] in Dataset[Datensatz]["df"].index:
            return clickData["points"][0]["hovertext"]
        return False
    return False


@app.callback([Output('Innovationsfrequenz', 'figure'), Output('Innovationsfrequenz_main', 'figure')],
              [Input('clickData', 'children'), Input("Datensatz", "value")])
def update_Details_Innovationsfrequenz(clickData, Datensatz):
    if clickData:
        data = Dataset[Datensatz]["Frequenz"][clickData]
        dataIssue = Dataset[Datensatz]["FrequenzIssue"][clickData]

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
        return (fig, fig)
    return ({}, {})


@ app.callback(Output('AnzahlPatente', 'children'),
               [Input('clickData', 'children'), Input("Datensatz", "value")])
def get_AnzahlPatente(clickData, Datensatz):
    if clickData:
        return "Anzahl Patente im Datensatz: " + str(Dataset[Datensatz]["df"].loc[clickData]["Anzahl Patente"])


@ app.callback(Output('Mean', 'children'),
               [Input('clickData', 'children'), Input("Datensatz", "value")])
def get_mean(clickData, Datensatz):
    if clickData:
        return "Durchschnittliche Anmeldezeit: " + Dataset[Datensatz]["qualitativ"].loc[clickData]["Mean Application Time"].strftime("%m/%d/%Y")


@ app.callback(Output('Median', 'children'),
               [Input('clickData', 'children'), Input("Datensatz", "value")])
def get_median(clickData, Datensatz):
    if clickData:
        return "Durchschnittliche Erteilungszeit: " + Dataset[Datensatz]["qualitativ"].loc[clickData]["Mean Issue Time"].strftime("%m/%d/%Y")


@ app.callback([Output('Innovationsniveau', 'figure'), Output('Innovationsniveau_main', 'figure')],
               [Input('clickData', 'children'), Input("Datensatz", "value")])
def update_Details_Innovationsniveau(clickData, Datensatz):
    if clickData:
        DataSelect = Dataset[Datensatz]["dfnumericnorm"][Dataset[Datensatz]["dfnumericnorm"]["company"]
                                                         == clickData]
        InnovationsniveauDF = DataSelect[["Anzahl Patente", "Zitationsrate", "Größte Zitationszahl",
                                          "Zitierhäufigkeit", "Patentzitationsindex", "hIndex", "Selbstzitationszahl", "Frühe Zitationen"]]
        fig = go.Figure()
        fig_main = go.Figure()

        fig.add_trace(go.Bar(
            x=list(InnovationsniveauDF.columns),
            y=[item for sublist in list(InnovationsniveauDF.values)
               for item in sublist],
            name=clickData,
            marker_color='#91C65D',

        ))
        fig_main.add_trace(go.Bar(
            y=["Patentzitationsindex", "hIndex", "Selbstzitationszahl"],
            x=[item for sublist in list(InnovationsniveauDF[["Patentzitationsindex", "hIndex", "Selbstzitationszahl"]].values)
               for item in sublist],
            name=clickData,
            marker_color='#91C65D',
            orientation='h'
        ))

        fig.add_trace(go.Bar(
            x=["Anzahl Patente", "Zitationsrate", "Größte Zitationszahl",
                "Zitierhäufigkeit", "Patentzitationsindex", "hIndex", "Selbstzitationszahl", "Frühe Zitationen"],
            y=Dataset[Datensatz]["meandata"][["Anzahl Patente", "Zitationsrate", "Größte Zitationszahl",
                                              "Zitierhäufigkeit", "Patentzitationsindex", "hIndex", "Selbstzitationszahl", "Frühe Zitationen"]].values,
            name="Durchschnitt im Datensatz",
            marker_color='gainsboro',

        ))
        fig_main.add_trace(go.Bar(
            y=["Patentzitationsindex", "hIndex", "Selbstzitationszahl"],
            x=Dataset[Datensatz]["meandata"][[
                "Patentzitationsindex", "hIndex", "Selbstzitationszahl"]].values,
            name="Durchschnitt im Datensatz",
            marker_color='gainsboro',
            orientation='h'
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
        fig_main.update_layout(margin=dict(l=30, r=30, b=20, t=40), hovermode='closest',
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

        return (fig, fig_main)
    else:
        return ({}, {})


@ app.callback(Output('CPC-Pie-Chart', 'figure'),
               [Input('clickData', 'children'), Input("Datensatz", "value")])
def update_Details_CPC(clickData, Datensatz):
    if clickData:
        DataSelect = Dataset[Datensatz]["dfnumericnorm"][Dataset[Datensatz]["dfnumericnorm"]["company"]
                                                         == clickData]
        InnovationspieDF = DataSelect[[
            "CPC - Refinement", "CPC - Combination", "CPC - Novel Combination", "CPC - Origination"]]

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=list(InnovationspieDF.columns),
            y=[item for sublist in list(InnovationspieDF.values)
               for item in sublist],
            name=clickData

        ))

        fig.add_trace(go.Bar(
            x=["CPC - Refinement", "CPC - Combination",
                "CPC - Novel Combination", "CPC - Origination"],
            y=Dataset[Datensatz]["meandata"][[
                "CPC - Refinement", "CPC - Combination", "CPC - Novel Combination", "CPC - Origination"]].values,
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
            title='CPC-Code Shares'
        )

        return fig
    else:
        return {}


@ app.callback([Output('Innovationsfähigkeit', 'figure'), Output('Innovationsfähigkeit_main', 'figure')],
               [Input('clickData', 'children'), Input("Datensatz", "value")])
def update_Details_Innovationsfähigkeit(clickData, Datensatz):
    if clickData:
        DataSelect = Dataset[Datensatz]["dfnumericnorm"][Dataset[Datensatz]["dfnumericnorm"]["company"]
                                                         == clickData]
        InnovationsfähigkeitDF = DataSelect[["Anzahl individueller Erfinder", "Anzahl individueller Erfinder/Patente", "Intensität der Zusammenarbeit",
                                             "Durchschnittliche Anzahl Erfinder pro Patent (Teamgröße)", "Price Law Key Inventor Amount", "Real Key Inventor Amount", "Anzahl Kooperationen"]]

        fig = go.Figure()
        fig_main = go.Figure()
        fig.add_trace(go.Bar(
            x=["individuelle Erfinder", "individuelle Erfinder/Patente", "Intensität der Zusammenarbeit",
                "Durchschnittliche Teamgröße", "Schlüsselerfinder (Price Law)", "Schlüsselerfinder (min. 3 Patente)", "Anzahl Kooperationen"],
            y=[item for sublist in list(InnovationsfähigkeitDF.values)
               for item in sublist],
            name=clickData,
            marker_color='#283A3E',
        ))
        fig_main.add_trace(go.Bar(
            y=["individuelle Erfinder", "Intensität der Zusammenarbeit",
                "Durchschnittliche Teamgröße"],
            x=[item for sublist in list(InnovationsfähigkeitDF[["Anzahl individueller Erfinder", "Intensität der Zusammenarbeit", "Durchschnittliche Anzahl Erfinder pro Patent (Teamgröße)"]].values)
               for item in sublist],
            name=clickData,
            marker_color='#283A3E',
            orientation='h'
        ))
        fig.add_trace(go.Bar(
            x=["individuelle Erfinder", "individuelle Erfinder/Patente", "Intensität der Zusammenarbeit",
                "Durchschnittliche Teamgröße", "Schlüsselerfinder (Price Law)", "Schlüsselerfinder (min. 3 Patente)", "Anzahl Kooperationen"],
            y=Dataset[Datensatz]["meandata"][["Anzahl individueller Erfinder", "Anzahl individueller Erfinder/Patente", "Intensität der Zusammenarbeit",
                                              "Durchschnittliche Anzahl Erfinder pro Patent (Teamgröße)", "Price Law Key Inventor Amount", "Real Key Inventor Amount", "Anzahl Kooperationen"]].values,
            name="Durchschnitt im Datensatz",
            marker_color='gainsboro',
        ))
        fig_main.add_trace(go.Bar(
            y=["individuelle Erfinder", "Intensität der Zusammenarbeit",
                "Durchschnittliche Teamgröße"],
            x=Dataset[Datensatz]["meandata"][["Anzahl individueller Erfinder", "Intensität der Zusammenarbeit",
                                              "Durchschnittliche Anzahl Erfinder pro Patent (Teamgröße)"]].values,
            name="Durchschnitt im Datensatz",
            marker_color='gainsboro',
            orientation='h'
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
            y=1,
            xanchor="right",
            x=1
        ),
            title='Innovationsfähigkeit '
        )
        fig_main.update_layout(margin=dict(l=30, r=30, b=20, t=40), hovermode='closest',
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
            title='Innovationsfähigkeit '
        )

        return fig, fig_main
    else:
        return {}, {}


@ app.callback([Output('Innovationscharakter', 'figure'), Output('Innovationscharakter_main', 'figure')],
               [Input('clickData', 'children'), Input("Datensatz", "value")])
def update_Details_Innovationscharakter(clickData, Datensatz):
    if clickData:
        DataSelect = Dataset[Datensatz]["dfnumericnorm"][Dataset[Datensatz]["dfnumericnorm"]["company"]
                                                         == clickData]
        InnovationscharakterDF = DataSelect[["Technologische Breite norm.",
                                             "TokenNovelty - Uniqueness", "Percentage Scientific Linkage", "Scientific Linkage Amount", "Claim Complexity", "Claims Uniqueness"]]

        fig = go.Figure()
        fig_main = go.Figure()
        fig.add_trace(go.Bar(
            x=["Technologische Breite norm.",
               "TokenNovelty - Uniqueness", "Percentage Scientific Linkage", "Scientific Linkage Amount"],
            y=[item for sublist in list(InnovationscharakterDF[["Technologische Breite norm.",
                                                                "TokenNovelty - Uniqueness", "Percentage Scientific Linkage", "Scientific Linkage Amount"]].values)
               for item in sublist],
            name=clickData,
            marker_color='#21A7E9',
        ))
        fig_main.add_trace(go.Bar(
            y=["Technologische Breite norm.",
                "Claim Complexity", "Claims Uniqueness"],
            x=[item for sublist in list(InnovationscharakterDF[["Technologische Breite norm.",
                                                                "Claim Complexity", "Claims Uniqueness"]].values)
               for item in sublist],
            name=clickData,
            marker_color='#21A7E9',
            orientation="h"
        ))

        fig.add_trace(go.Bar(
            x=["Technologische Breite norm.",
               "TokenNovelty - Uniqueness", "Percentage Scientific Linkage", "Scientific Linkage Amount"],
            y=Dataset[Datensatz]["meandata"][["Technologische Breite norm.",
                                              "TokenNovelty - Uniqueness", "Percentage Scientific Linkage", "Scientific Linkage Amount"]].values,
            name="Durchschnitt im Datensatz",
            marker_color='gainsboro',
        ))
        fig_main.add_trace(go.Bar(
            y=["Technologische Breite norm.",
                "Claim Complexity", "Claims Uniqueness"],
            x=Dataset[Datensatz]["meandata"][[
                "Technologische Breite norm.", "Claim Complexity", "Claims Uniqueness"]].values,
            name="Durchschnitt im Datensatz",
            marker_color='gainsboro',
            orientation="h"
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
        fig_main.update_layout(margin=dict(l=30, r=30, b=20, t=40), hovermode='closest',
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

        return fig, fig_main
    else:
        return {}, {}


@ app.callback(Output('Innovationscharakter - Claims', 'figure'),
               [Input('clickData', 'children'), Input("Datensatz", "value")])
def update_Details_Innovationscharakter(clickData, Datensatz):
    if clickData:
        DataSelect = Dataset[Datensatz]["dfnumericnorm"][Dataset[Datensatz]["dfnumericnorm"]["company"]
                                                         == clickData]
        InnovationscharakterDF = DataSelect[["Claim Length Value Index", "1st Claim length", "Claim Complexity Value Index",
                                             "Claim Complexity", "Claim Amount Value Index", "Claim Amount", "Claims Uniqueness"]]

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=["Claim Length Value Index", "1st Claim length", "Claim Complexity Value Index",
                "Claim Complexity", "Claim Amount Value Index", "Claim Amount", "Claims Uniqueness"],
            y=[item for sublist in list(InnovationscharakterDF.values)
               for item in sublist],
            name=clickData,
            marker_color='#21A7E9',
        ))

        fig.add_trace(go.Bar(
            x=["Claim Length Value Index", "1st Claim length", "Claim Complexity Value Index",
                "Claim Complexity", "Claim Amount Value Index", "Claim Amount", "Claims Uniqueness"],
            y=Dataset[Datensatz]["meandata"][["Claim Length Value Index", "1st Claim length", "Claim Complexity Value Index",
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
            y=1.0,
            xanchor="right",
            x=1
        ),
            title='Innovationscharakter - Claims'
        )

        return fig
    else:
        return {}


@ app.callback(Output('KindCode-Pie-Chart', 'figure'),
               [Input('clickData', 'children'), Input("Datensatz", "value")])
def update_Details_CPC(clickData, Datensatz):
    if clickData:
        DataSelect = Dataset[Datensatz]["dfnumericnorm"][Dataset[Datensatz]["dfnumericnorm"]["company"]
                                                         == clickData]
        InnovationspieDF = DataSelect[[
            "B1 - Anteil", "B2 - Anteil", "A - Anteil", "C1 - Anteil"]]

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=list(InnovationspieDF.columns),
            y=[item for sublist in list(InnovationspieDF.values)
               for item in sublist],
            name=clickData

        ))

        fig.add_trace(go.Bar(
            x=["B1 - Anteil", "B2 - Anteil", "A - Anteil", "C1 - Anteil"],
            y=Dataset[Datensatz]["meandata"][[
                "B1 - Anteil", "B2 - Anteil", "A - Anteil", "C1 - Anteil"]].values,
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
            title='KindCode Shares'
        )

        return fig
    else:
        return {}


@ app.callback(Output('Kooperationen-table', 'data'),
               [Input('clickData', 'children'), Input("Datensatz", "value")])
def update_table(clickData, Datensatz):
    if clickData:
        if clickData in Dataset[Datensatz]["kooperationen"].index:
            data = Dataset[Datensatz]["kooperationen"].loc[[
                clickData]]
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
               [Input('clickData', 'children'), Input("Datensatz", "value")])
def display_hover_data(clickData, Datensatz):
    if clickData:
        keyinventors = Dataset[Datensatz]["qualitativ"].loc[clickData]["Key Inventor Names"]
        if type(keyinventors) == list:
            return "Schlüsselerfinder: " + " ".join(keyinventors)
        else:
            return "Nicht genügend Daten über Erfinder vorhanden."


@ app.callback(Output('DetailsUniqueTerms', 'children'),
               [Input('clickData', 'children'), Input("Datensatz", "value")])
def display_hover_data(clickData, Datensatz):
    if clickData:
        return " Top 30 Unique Terms: " + ", ".join(Dataset[Datensatz]["qualitativ"].loc[clickData]["Uniqueterms Walther"][:30])


@ app.callback(Output('maininfo-table', 'data'),
               [Input('clickData', 'children'), Input("Datensatz", "value")])
def update_infotable(clickData, Datensatz):
    if clickData:
        if clickData in Dataset[Datensatz]["Finanzdaten"].index:
            data = Dataset[Datensatz]["Finanzdaten"][["BvD ID Nummer", "Stand", "Globale KM - Name", "Gesellschafter - NACE,Textbeschreibung"]].loc[[
                clickData]]
            return data.to_dict('records')
        else:
            return [{"BvD ID Nummer": "Keine Daten vorhanden", "Letztes verf. Jahr": "Keine Daten vorhanden", "Globale KM - Name": "Keine Daten vorhanden", "Gesellschafter - NACE,Textbeschreibung": "Keine Daten vorhanden"}]
    else:
        return [{"BvD ID Nummer": "Keine Daten vorhanden", "Letztes verf. Jahr": "Keine Daten vorhanden", "Globale KM - Name": "Keine Daten vorhanden", "Gesellschafter - NACE,Textbeschreibung": "Keine Daten vorhanden"}]


@ app.callback(Output('finance-table-eigenkapital', 'data'),
               [Input('clickData', 'children'), Input("Datensatz", "value")])
def update_infotable(clickData, Datensatz):
    if clickData:
        if clickData in Dataset[Datensatz]["Finanzdaten"].index:
            data = Dataset[Datensatz]["Finanzdaten"][["Eigenkapital tsd. EUR", "Fremd- zu Eigenkapital (%)", "Eigenkapitalquote (%)", "ROE vor Steuern (%)", "ROCE vor Steuern (%)", "Langfristige Verbindlichkeiten tsd. EUR", "EBITDA tsd. EUR",  "Cashflow tsd. Euro"]].loc[[
                clickData]]
            return data.to_dict('records')
        else:
            return [{"BvD ID Nummer": "Keine Daten vorhanden", "Letztes verf. Jahr": "Keine Daten vorhanden", "Globale KM - Name": "Keine Daten vorhanden", "Gesellschafter - NACE,Textbeschreibung": "Keine Daten vorhanden"}]
    else:
        return [{"BvD ID Nummer": "Keine Daten vorhanden", "Letztes verf. Jahr": "Keine Daten vorhanden", "Globale KM - Name": "Keine Daten vorhanden", "Gesellschafter - NACE,Textbeschreibung": "Keine Daten vorhanden"}]


@ app.callback(Output('finance-table-overview', 'data'),
               [Input('clickData', 'children'), Input("Datensatz", "value")])
def update_infotable(clickData, Datensatz):
    if clickData:
        if clickData in Dataset[Datensatz]["Finanzdaten"].index:
            data = Dataset[Datensatz]["Finanzdaten"][["Stand", "Anzahl Mitarbeiter", "Betriebsertrag/Jahr tsd. Euro", "Gewinn/Verlust vor Steuern tsd. EUR", "Gewinn pro Mitarbeiter tsd. EUR", "F&E Ausgaben tsd. EUR"]].loc[[
                clickData]]
            return data.to_dict('records')
        else:
            return [{"BvD ID Nummer": "Keine Daten vorhanden", "Letztes verf. Jahr": "Keine Daten vorhanden", "Globale KM - Name": "Keine Daten vorhanden", "Gesellschafter - NACE,Textbeschreibung": "Keine Daten vorhanden"}]
    else:
        return [{"BvD ID Nummer": "Keine Daten vorhanden", "Letztes verf. Jahr": "Keine Daten vorhanden", "Globale KM - Name": "Keine Daten vorhanden", "Gesellschafter - NACE,Textbeschreibung": "Keine Daten vorhanden"}]


@ app.callback(Output('CPC-table', 'data'),
               [Input('clickData', 'children'), Input("Datensatz", "value")])
def update_table(clickData, Datensatz):
    if clickData:
        if clickData in Dataset[Datensatz]["qualitativ"][["Codestext"]].index:
            data = Dataset[Datensatz]["qualitativ"][["Codestext"]].loc[[
                clickData]]
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
