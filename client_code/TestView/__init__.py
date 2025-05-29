from ._anvil_designer import TestViewTemplate
from anvil import *
from ..OrganigrammeHtml import OrganigrammeHtml  # ✅ Assure-toi que le nom est correct

from anvil.js.window import drawGraph

class TestView(TestViewTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

    # Exemple de données simples
    data = {
      "nodes": [
        {"id": 1, "label": "Node 1"},
        {"id": 2, "label": "Node 2"},
        {"id": 3, "label": "Node 3"}
      ],
      "edges": [
        {"from": 1, "to": 2},
        {"from": 2, "to": 3}
      ]
    }

    # Appel de la fonction JS
    drawGraph(data)



