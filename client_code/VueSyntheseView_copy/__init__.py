from ._anvil_designer import VueSyntheseView_copyTemplate
from anvil import *
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from ...OrganigrammeHtml import OrganigrammeHtml

class VueSyntheseView_copy(VueSyntheseView_copyTemplate):
  def __init__(self, dossier, **properties):
    self.init_components(**properties)
    self.dossier = dossier

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

    self.organigramme = OrganigrammeHtml()
    self.add_component(self.organigramme)

  def form_show(self, **event_args):
    self.organigramme.call_js("drawGraph", self.graph_data)
