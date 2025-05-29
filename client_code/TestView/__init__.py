from ._anvil_designer import TestViewTemplate
from anvil import *

class TestView(TestViewTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

    # ➕ Données statiques à afficher
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
    self.call_js("drawGraph", self.graph_data)


