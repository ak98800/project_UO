from anvil import *
import anvil.js
import anvil.js.window

class TestView(TestViewTemplate):

  def __init__(self, **properties):
    self.init_components(**properties)

    # Données du graphe
    data = {
      "nodes": [
        {"id": 1, "label": "Départ"},
        {"id": 2, "label": "Étape 1"},
        {"id": 3, "label": "Étape 2"}
      ],
      "edges": [
        {"from": 1, "to": 2},
        {"from": 2, "to": 3}
      ]
    }

    # Appel de la fonction JS après un court délai (important)
    anvil.js.call_later(0.1, lambda: anvil.js.window.drawGraph(data))




