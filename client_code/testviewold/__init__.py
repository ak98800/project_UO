from ._anvil_designer import TestViewTemplate
from anvil import *
from ..OrganigrammeHtml import OrganigrammeHtml

class TestView(TestViewTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

    # ➕ Crée l'organigramme
    self.organigramme = OrganigrammeHtml()
    self.add_component(self.organigramme)

    # ➕ Prépare des données statiques
    self.graph_data = {
      "nodes": [
        {"id": 1, "label": "Société Mère"},
        {"id": 2, "label": "Filiale A"},
        {"id": 3, "label": "Filiale B"}
      ],
      "edges": [
        {"from": 1, "to": 2},
        {"from": 1, "to": 3}
      ]
    }

  def form_show(self, **event_args):
    print("Données prêtes, appel JS...")
    self.organigramme.call_js("drawGraph", self.graph_data)
