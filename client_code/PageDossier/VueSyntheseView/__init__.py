from ._anvil_designer import VueSyntheseViewTemplate
from anvil import *
import anvil.server
from ...OrganigrammeHtml import OrganigrammeHtml

class VueSyntheseView(VueSyntheseViewTemplate):
  def __init__(self, dossier, **properties):
    self.init_components(**properties)
    self.dossier = dossier

    # 1. Charger le graphe
    self.graph_data = anvil.server.call("get_graph_data_for_dossier", self.dossier["id"])

    # 2. Injecter le HTML avec le slot JS
    self.organigramme = OrganigrammeHtml()
    self.content_panel.clear()
    self.content_panel.add_component(self.organigramme)

  def form_show(self, **event_args):
    self.organigramme.call_js("drawGraph", self.graph_data)






