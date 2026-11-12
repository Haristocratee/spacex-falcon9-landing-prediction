# Importer les bibliothèques nécessaires
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Lire les données de lancements SpaceX dans un dataframe pandas
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Liste des sites de lancement (pour les options du menu déroulant)
launch_sites = sorted(spacex_df['Launch Site'].unique())

# Créer l'application Dash
app = dash.Dash(__name__)

# Créer la mise en page de l'application
app.layout = html.Div(children=[html.H1('Tableau de bord des lancements SpaceX',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TÂCHE 1 : ajouter un menu déroulant pour choisir le site de lancement
                                # La valeur par défaut correspond à TOUS les sites
                                dcc.Dropdown(id='site-dropdown',
                                             options=[{'label': 'Tous les sites', 'value': 'ALL'}] +
                                                     [{'label': site, 'value': site} for site in launch_sites],
                                             value='ALL',
                                             placeholder="Sélectionnez un site de lancement",
                                             searchable=True),
                                html.Br(),

                                # TÂCHE 2 : ajouter un diagramme circulaire du nombre total de lancements réussis pour tous les sites
                                # Si un site précis est sélectionné, afficher le nombre de succès et d'échecs de ce site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Plage de charge utile (kg) :"),
                                # TÂCHE 3 : ajouter un curseur pour sélectionner la plage de charge utile
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                marks={i: f'{i}' for i in range(0, 10001, 2500)},
                                                value=[min_payload, max_payload]),

                                # TÂCHE 4 : ajouter un nuage de points montrant la corrélation entre charge utile et succès du lancement
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TÂCHE 2 :
# Fonction de rappel (callback) avec `site-dropdown` en entrée et `success-pie-chart` en sortie
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        # Tous les sites : total des lancements réussis (class = 1) par site
        fig = px.pie(spacex_df, values='class', names='Launch Site',
                     title='Total des lancements réussis par site')
    else:
        # Site précis : nombre de succès et d'échecs
        site_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        counts = site_df['class'].value_counts().rename_axis('class').reset_index(name='count')
        counts['Issue'] = counts['class'].map({1: 'Succès', 0: 'Échec'})
        fig = px.pie(counts, values='count', names='Issue',
                     title=f'Total des lancements réussis pour le site {entered_site}')
    return fig

# TÂCHE 4 :
# Fonction de rappel avec `site-dropdown` et `payload-slider` en entrées et `success-payload-scatter-chart` en sortie
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
               Input(component_id='payload-slider', component_property='value')])
def get_scatter_chart(entered_site, payload_range):
    low, high = payload_range
    # Filtrer sur la plage de charge utile
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= low) &
                            (spacex_df['Payload Mass (kg)'] <= high)]
    if entered_site == 'ALL':
        title = 'Corrélation entre charge utile et succès pour tous les sites'
    else:
        filtered_df = filtered_df[filtered_df['Launch Site'] == entered_site]
        title = f'Corrélation entre charge utile et succès pour le site {entered_site}'
    fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class',
                     color='Booster Version Category', title=title,
                     labels={'class': 'Succès (1) / Échec (0)'})
    return fig


# Lancer l'application
if __name__ == '__main__':
    app.run()
