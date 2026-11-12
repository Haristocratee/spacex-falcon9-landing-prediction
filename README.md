# SpaceX Falcon 9 : prédiction de l'atterrissage du premier étage

Projet final de science des données (IBM). Objectif : prédire si le premier étage d'un Falcon 9 atterrira, afin d'estimer le coût d'un lancement.

## Contenu

| Dossier | Fichier | Rôle |
|---|---|---|
| `notebooks/` | `01_collecte_api_spacex.ipynb` | Collecte via l'API SpaceX |
| | `02_data_wrangling.ipynb` | Nettoyage et étiquetage (`Class`) |
| | `03_eda_sql.ipynb` | Analyse exploratoire avec SQL (SQLite) |
| | `04_eda_visualisation.ipynb` | EDA avec Matplotlib/Seaborn et feature engineering |
| | `05_carte_folium.ipynb` | Carte interactive des sites de lancement |
| | `06_prediction_ml.ipynb` | Régression logistique, SVM, arbre, KNN (GridSearchCV) |
| `app/` | `spacex-dash-app.py` | Tableau de bord Plotly Dash |
| `presentation/` | `Projet_final_SpaceX_Falcon9.pdf` / `.pptx` | Présentation de synthèse |

## Lancer le tableau de bord

```bash
pip install -r requirements.txt
# placer spacex_launch_dash.csv dans le dossier app/
python app/spacex-dash-app.py   # http://127.0.0.1:8050
```

## Notes
- Les notebooks 4 à 6 et l'application Dash sont en français. Les notebooks 1 à 3 sont en anglais.
- Les notebooks 1, 2, 4, 5 et 6 sont écrits pour JupyterLite (`piplite`, `from js import fetch`). Dans Colab ou Jupyter classique, remplacer par `pd.read_csv(URL)`.
- Exécuter chaque notebook (« Run All ») avant de pousser pour enregistrer les sorties.
