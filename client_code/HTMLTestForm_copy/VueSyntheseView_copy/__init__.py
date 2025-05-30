from ._anvil_designer import VueSyntheseView_copyTemplate
from anvil import *
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ...HTMLTestForm import HTMLTestForm
from anvil.tables import app_tables
import anvil.server

class VueSyntheseView_copy(VueSyntheseView_copyTemplate):
  def __init__(self, nom_dossier=None, **properties):
    self.init_components(**properties)

    # Récupérer les dossiers
    self.dossiers_disponibles = anvil.server.call('get_dossiers_disponibles')
    self.dropdown_dossier.items = self.dossiers_disponibles

    # Ajouter le HTMLTestForm au layout
    self.form_test = HTMLTestForm()
    self.add_component(self.form_test)

  def btn_afficher_graph_click(self, **event_args):
    nom_dossier = self.dropdown_dossier.selected_value

    if not nom_dossier:
      alert("Veuillez sélectionner un dossier.")
      return

    relations = anvil.server.call('get_relations_dossier', nom_dossier)

    noms_uniques = set()
    edges = []

    for actionnaire, societe, pourcentage in relations:
      noms_uniques.add(actionnaire)
      noms_uniques.add(societe)
      edges.append({
        "from": actionnaire,
        "to": societe,
        "label": f"{pourcentage}%",
        "font": { "align": "middle" }
      })

    nodes = [{"id": name, "label": name} for name in noms_uniques]

    # Appel JS pour dessiner le graphe
    self.form_test.call_js('drawGraph', nodes, edges)
