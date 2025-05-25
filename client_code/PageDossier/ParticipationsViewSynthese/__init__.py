from ._anvil_designer import ParticipationsViewSyntheseTemplate
from anvil import *
import anvil.server
from anvil.tables import app_tables
import pandas as pd

class ParticipationsViewSynthese(ParticipationsViewSyntheseTemplate):
  def __init__(self, dossier, **properties):
    self.init_components(**properties)
    self.dossier = dossier
    self.charger_donnees()

  def charger_donnees(self):
    # Recherche des participations pour ce dossier
    lignes = app_tables.participations.search(folder=self.dossier)
    df = pd.DataFrame([{
      "societe": l["societe"],
      "actionnaire": l["actionnaire"],
      "pourcentage": l["pourcentage"]
    } for l in lignes if l["societe"] and l["actionnaire"]])

    if df.empty:
      self.repeating_synthese.items = []
      return

    # Regroupement par société
    regroupement = df.groupby("societe").agg({
      "actionnaire": pd.Series.nunique,
      "pourcentage": "sum"
    }).reset_index()

    # Détermination du statut visuel
    def calcul_statut(pct):
      if abs(pct - 100) <= 1e-2:
        return "green"
      elif pct < 100:
        return "orange"
      else:
        return "red"

    regroupement["statut"] = regroupement["pourcentage"].apply(calcul_statut)

    # Ajout du dossier pour chaque ligne (utile pour le clic)
    regroupement["dossier"] = self.dossier

    # Envoi au composant
    self.repeating_synthese.items = regroupement.to_dict("records")
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users

class ParticipationsViewSynthese(ParticipationsViewSyntheseTemplate):
  def __init__(self, dossier, **properties):
    self.init_components(**properties)
    self.dossier = dossier



    # Données temporaires
    self.repeating_participations.items = [
      {
        "societe": "SEB",
        "actionnaire": "Holding ANIS",
        "pourcentage": 51,
        "type": "PP",
        "groupe": "Agro",
        "sous_groupe": "Pain"
      },
      {
        "societe": "SEM",
        "actionnaire": "Holding ANIS",
        "pourcentage": 49,
        "type": "PP",
        "groupe": "Meunerie",
        "sous_groupe": "Farine"
      }
    ]

  def text_2_show(self, **event_args):
    """This method is called when the component is shown on the screen."""
    pass
