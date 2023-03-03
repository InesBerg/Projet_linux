# -*- coding: utf-8 -*-
"""
Created on Wed Mar  1 11:19:19 2023

@author: inesb
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from dash import Dash, html, dcc
from dash.dependencies import Output, Input
import datetime as dt
from datetime import datetime, time
import numpy as np


df=pd.read_csv("//wsl.localhost/Ubuntu/home/inesbergaut/prix_lvmh.csv", sep=",", header=None)
df.columns = ['Date','Action LVMH']

app = Dash(__name__) #objet de type dash
app.title = 'Action LVMH'
df['Date'] = pd.to_datetime(df['Date'])
df = df.set_index("Date")
print(df)
'''
#graphique évolution du cours de l'action dans la journée
start_time = dt.time(hour=9, minute=0)
end_time = dt.time(hour=17, minute=30)
df = df[(df['Heure'].dt.time >= start_time) & (df['Heure'].dt.time <= end_time)]
fig = go.Figure()
fig.add_trace(go.Scatter(x=df['Heure'], y=df['Prix LVMH'], mode='lines'))
'''
#App layout

app.layout=html.Div([
    
    #Titre
    html.H2(
       "ACTION LVMH",
       style={"marginTop": 5, "marginLeft": "10px"},
   ),
    
    html.H3(
        "Secteur : Habillement et accessoires",
        style={"marginLeft": "10px"},
    ),
    
    html.H3(
        "Indice de référence : CAC 40",
        style={"marginLeft": "10px"},
    ),
    
   #Prix de l'action LVMH
    html.Div(id='action_lvmh', style={'padding': '40px', 'font-size': '30px'}),
    
    html.H4("EURONEXT PARIS DONNEES TEMPS REEL",style={"marginLeft": "10px"}),
    
    
    #sélectionner de date
    dcc.DatePickerSingle(
        id='date-picker',
        min_date_allowed=df.index.min(),
        max_date_allowed=df.index.max(),
        initial_visible_month=dt.date.today(),
        date=dt.date.today()
    ),
    
    # Graphique
    dcc.Graph(id="graph"),
    
    #Prix de clôture de l'action LVMH
    #html.H1(id="prix-closure"),
   
    #Mise à jour automatique toutes les minutes
    dcc.Interval(
        id='interval-min',
        interval=1*60*1000,  # Mettre à jour toutes les 1 minute
        n_intervals=0
    ),
    
    # Mise à jour automatique à 18h tous les jours
    dcc.Interval(
        id='interval-jour',
        interval=24*60*60*1000, # en millisecondes
        n_intervals=0
    ),
    
    html.H1('Prix le plus haut et le plus bas'),
    
    html.Div(id='output-container')
    
    ],
    
    style={
        "backgroundColor": "#f2f2f2",
        "height": "1000vh"
    }
    
    )

#Callback pour mettre à jour le prix de l'action en temps réel
@app.callback(Output('action_lvmh', 'children'),
              [Input('interval-min', 'n_intervals')])
def update_price(n):
    # Faire une requête pour récupérer le nouveau prix (remplacer par votre propre code)
    new_price = df['Action LVMH'].iloc[-1]
    
    # Formater le prix pour l'affichage
    formatted_price = '{:.2f} €'.format(new_price)
    
    # Mettre à jour le contenu de l'élément html avec le nouveau prix
    return formatted_price

#Callback pour mettre à jour le graphique représentant le prix de l'action en temps réel
@app.callback(
    Output("graph", "figure"),
    [Input('date-picker', 'date'),
     Input('interval-min', 'n_intervals')]
)
def update_graph(selected_date, n):
    # Conversion de la date sélectionnée au format datetime
    selected_date = dt.datetime.strptime(selected_date, "%Y-%m-%d").date()
    
    # Filtrage des données pour la date sélectionnée
    df_selected = df[df.index.date == selected_date]
    
    # Création du graphique
    fig = {
        "data": [
            {"x": df_selected.index, "y": df_selected["Action LVMH"], "type": "line", "name": "Prix de l'action"}
        ],
        "layout": {
            "title": "Prix de l'action LVMH le {}".format(selected_date.strftime("%d/%m/%Y")),
            "xaxis": {"title": "Heure"},
            "yaxis": {"title": "Prix ($)"},
            "margin": {"l": 40, "r": 40, "t": 80, "b": 40}
        }
    }
    
    return fig

'''
#Callback pour mettre à jour le prix de clôture de l'action tous les jours à 18h
@app.callback(
    Output("prix-closure", "children"),
    [Input('interval-jour', 'n_intervals')]
)
def update_prix_closure(n):
    # Récupération de la date d'aujourd'hui
    today = dt.date.today()
    
    # Filtrage des données pour la date d'hier
    yesterday = today - dt.timedelta(days=1)
    data = df[df.index.date == yesterday]
    
    # Récupération du prix de clôture
    prix_closure = data["Action LVMH"].iloc[-1]
    
    # Affichage du prix de clôture
    return f"Prix de clôture pour le {yesterday.strftime('%d/%m/%Y')} : {prix_closure} €"
'''
# Définition de la fonction de mise à jour des prix
@app.callback(
    Output(component_id='output-container', component_property='children'),
    Input(component_id='date-picker', component_property='date')
)
def update_output_div(date_string):
    selected_date = datetime.strptime(date_string, '%Y-%m-%d')
    start_time = datetime.combine(selected_date, time(hour=9))
    end_time = datetime.combine(selected_date, time(hour=18))
    filtered_df = df.loc[start_time:end_time]
    if len(filtered_df) > 0:
        highest_price = filtered_df['Action LVMH'].max()
        lowest_price = filtered_df['Action LVMH'].min()
        return f'Le prix le plus haut est {highest_price} et le prix le plus bas est {lowest_price}'
    else:
        return 'Aucune donnée pour cette journée'

if __name__ == '__main__':
    app.run_server(debug=True)