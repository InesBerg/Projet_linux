# -*- coding: utf-8 -*-
"""
Created on Wed Mar  1 11:19:19 2023
@author: inesb
"""

import pandas as pd
from dash import Dash, html, dcc
from dash.dependencies import Output, Input
import datetime as dt
from datetime import datetime, time, timedelta
import numpy as np


df=pd.read_csv("//wsl.localhost/Ubuntu/home/inesbergaut/prix_lvmh.csv", sep=",", header = None)
df.columns=['Date','Heure','Action LVMH']
df['Date'] = pd.to_datetime(df['Date'])
df['Heure'] = df['Heure'].apply(lambda x: datetime.strptime(x, '%H:%M').time())

dates = df['Date'].dt.date.unique()

previous_variation=None

def get_last_close_price():
    # Obtention de la date actuelle
    current_time = dt.datetime.now()
    # Si c'est un week-end, obtenir la dernière valeur de clôture de vendredi
    if current_time.weekday() == 5: # Samedi
        last_close_price = df[df['Date'].dt.weekday == 4]['Action LVMH'].iloc[-1]
    elif current_time.weekday() == 6: # Dimanche
        last_close_price = df[df['Date'].dt.weekday == 4]['Action LVMH'].iloc[-1]
    else:
        # Si c'est un jour de semaine, obtenir la dernière valeur de clôture pour cette journée
        last_close_price = df[df['Date'].dt.date == current_time.date()]['Action LVMH'].iloc[-1]
    return last_close_price

app = Dash(__name__) #objet de type dash
app.title = 'Action LVMH'


#App layout

app.layout=html.Div([
    
    html.Div(style={'backgroundColor': '#9E6A44', 'height': '100px'}),
    
    #Titre
    html.H1(
       "LVMH",
       style={"position": "absolute", "top": "0%", "left": "50%", "transform": "translate(-50%, -50%)","font-size": "50px",
                'textDecoration': 'underline'},
   ),
    
    html.P(
                'MOËT HENNESSY.LOUIS VUITTON',
                style={
                    'textAlign': 'center',
                    'fontSize': '20px',
                    'marginTop': '-40px'
                }
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
    html.Div(id='action_lvmh', style={'padding': '20px', 'font-size': '30px'}),
    
    #Pourcentage de variation par rapport au prix de clôture
    html.Div([
            html.Div(
                id="variation",
                style={
                    'font-size': '25px',
                    'padding': '0.06px',
                    'margin': '10px',
                    'width': '200px',
                    'height': '100px',
                    'display': 'flex',
                    'justify-content': 'center',
                    'align-items': 'center'
                },
            )
        ],
        style={'position': 'absolute', 'left': 80, 'top': 200},   
    ),
    
    html.H4("EURONEXT PARIS DONNEES TEMPS REEL",style={"marginLeft": "10px"}),
    
    
    html.H2('Cours de bourse LVMH',style={"marginLeft": "10px"}),
    
    html.Label('Choisir une date '),
    
    dcc.DatePickerSingle(
        id='date-picker',
        min_date_allowed=min(dates),
        max_date_allowed=max(dates),
        initial_visible_month=max(dates),
        display_format='DD/MM/YYYY',
        date=max(dates),
        style={'backgroundColor': '#f2f2f2'} ,
    ),
    
    html.Div(
           dcc.Graph(
               id='graph',
           ),
           style={'margin-left': 'auto', 'margin-right': 'auto', 'width': '90%'}
       ),
    
    #dcc.Graph(id='graph', style={'margin-left': 'auto', 'margin-right': 'auto', 'width': '50%'}),
    
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
    
    
    html.Div([
         html.Div([
                 html.H3("Prix le plus haut"),
                 html.Div(
                     id='highest-price',
                     style={
                         'font-size': '25px',
                         'padding': '0.06px',
                         'margin': '1px',
                         'width': '200px',
                         'height': '50px',
                         'display': 'flex',
                         'justify-content': 'center',
                         'align-items': 'center'
                     },
                 )
             ],
             style={'position': 'absolute', 'right': 500, 'top': 150},
             
         ),
         html.Div([
                 html.H3("Prix le plus bas"),
                 html.Div(
                     id='lowest-price',
                     style={
                         'font-size': '25px',
                         'padding': '0.06px',
                         'margin': '1px',
                         'width': '200px',
                         'height': '50px',
                         'display': 'flex',
                         'justify-content': 'center',
                         'align-items': 'center'
                     },
                 )
             ],
            style={'position': 'absolute', 'right': 300, 'top': 150},
         ),
         
         #Prix de clôture de l'action LVMH
         html.Div([
                 html.H3("Dernier prix de clôture"),
                 html.Div(
                     id="prix-closure",
                     style={
                         'font-size': '25px',
                         'padding': '0.06px',
                         'margin': '1px',
                         'width': '200px',
                         'height': '50px',
                         'display': 'flex',
                         'justify-content': 'center',
                         'align-items': 'center'
                     },
                 )
             ],
             style={'position': 'absolute', 'right': 100, 'top': 150},   
         ),
         
         #Volatilité de l'action LVMH
         html.Div([
                 html.H3("Volatilité"),
                 html.Div(
                     id='volatility',
                     style={
                         'font-size': '25px',
                         'padding': '0.06px',
                         'margin': '1px',
                         'width': '200px',
                         'height': '50px',
                         'display': 'flex',
                         'justify-content': 'center',
                         'align-items': 'center'
                     },
                 )
             ],
            style={'position': 'absolute', 'right': 500, 'top': 270},
         ),
         
     ],
 ),
    
    ],
    
    style={
        "backgroundColor": "#E6C19C",
        "min-height": "100vh"}
    
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

# Définition de la fonction de mise à jour du graphique en fonction de la date sélectionnée
@app.callback(Output('graph', 'figure'),
              [Input('date-picker', 'date'),
               Input('interval-min', 'n_intervals')])

def update_graph(selected_date, n):
    # Recharger les données du fichier CSV
    df=pd.read_csv("//wsl.localhost/Ubuntu/home/inesbergaut/prix_lvmh.csv", sep=",", header = None)
    df.columns=['Date','Heure','Action LVMH']
    df['Date'] = pd.to_datetime(df['Date'])
    df['Heure'] = df['Heure'].apply(lambda x: datetime.strptime(x, '%H:%M').time())
    df = df[df['Date'] == selected_date]
    
    heures = np.arange(9, 19, 1)
    selected_date_title = datetime.strptime(selected_date, '%Y-%m-%d').strftime('%d/%m/%Y')
    # Créer le graphique
    figure = {
        'data': [{'x': df['Heure'], 'y': df['Action LVMH'], 'type': 'line','line': {'color': 'rgb(165,42,42)'}}],
        'layout': {'title': f'Cours de l\'action LVMH le {selected_date_title}',
                  'xaxis': {'title': 'Heure',
                             'tickmode': 'array',
                             'tickvals': [datetime.strptime(h, '%H').time() for h in map(str, heures)],
                             'ticktext': [h.strftime('%H:%M') for h in [datetime.strptime(h, '%H').time() for h in map(str, heures)]]
                             
                             },
                   
                   'plot_bgcolor': '#f2f2f2'
                  }
    }
    
    
    return figure

#Callback pour mettre à jour le prix de clôture de l'action tous les jours à 18h
@app.callback(
    Output("prix-closure", "children"),
    [Input('interval-jour', 'n_intervals')]
)
def update_prix_closure(n):
   
    # Obtention de la dernière valeur de clôture de la journée
    last_close_price = get_last_close_price()
    # Formatage du prix de clôture avec 2 décimales
    formatted_price = "{:.2f}".format(last_close_price)
    # Retourner le prix de clôture mis à jour
    return f"{formatted_price} €"



# Définition de la fonction de mise à jour du prix le plus haut et le plus bas
@app.callback(
    [Output('highest-price', 'children'),
     Output('lowest-price', 'children')],
    Input('date-picker', 'date')
)
def update_output_div(date_string):
    selected_date = datetime.strptime(date_string, '%Y-%m-%d')
    start_time = dt.time(hour=9, minute=0)
    end_time = dt.time(hour=18, minute=0)
    filtered_df = df.loc[(df['Date'] == selected_date) & (df['Heure'] >= start_time) & (df['Heure'] <= end_time)]
    if len(filtered_df) > 0:
        highest_price = filtered_df['Action LVMH'].max()
        lowest_price = filtered_df['Action LVMH'].min()
        return f"{highest_price} €", f"{lowest_price} €"
    else:
        return 'Aucune donnée pour cette journée', 'Aucune donnée pour cette journée'


# Définir la fonction de mise à jour de la variation du prix actuel par rapport au prix de clôture de la veille
@app.callback(
    Output('variation', 'children'),
    Input('interval-min', 'n_intervals')
)
def update_variation(n):
    global previous_variation
    
    current_time = datetime.now().time()
    start_time = time(9, 0)
    end_time = time(18, 0)
    
    if current_time >= start_time and current_time <= end_time and datetime.today().weekday() < 5:
    # Récupération de la date d'aujourd'hui
        today = dt.date.today()
    
    # Filtrage des données pour la date d'hier
        yesterday = today - dt.timedelta(days=1)
        data = df[df['Date'].dt.date == yesterday]
    
    # Récupération du prix de clôture
        prix_closure = data["Action LVMH"].iloc[-1]
    
    # Récupérer la variation la plus récente
        variation_pct = ((df['Action LVMH'].iloc[-1]-prix_closure)/prix_closure)*100
        color = 'green' if variation_pct >= 0 else 'red'
        return html.Span(f"{variation_pct:.2f}%", style={'color': color})

# Définir la fonction de mise à jour de la volatilité
@app.callback(Output('volatility', 'children'), [Input('date-picker', 'date')])
def update_volatility(selected_date):
    # Sélectionner les données pour la date sélectionnée
    selected_data = df[df['Date'] == selected_date]
    
    # Calculer les rendements de l'action
    selected_data['Rendement'] = selected_data['Action LVMH'].pct_change()
    
    # Calculer la volatilité
    volatility = selected_data['Rendement'].std() * (252 ** 0.5)
    
    return "{:.2f}%".format(volatility * 100)


if __name__ == '__main__':
    app.run_server(debug=True)