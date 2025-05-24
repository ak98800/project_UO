from ._anvil_designer import ParticipationsViewTemplate
from anvil import *

class ParticipationsView(ParticipationsViewTemplate):
  def __init__(self, dossier, **properties):
    self.init_components(**properties)
    self.dossier = dossier

    # Entêtes
    self.header_panel.clear()
    self.header_panel.add_component(Label(text="Société", bold=True, width="15%"))
    self.header_panel.add_component(Label(text="Actionnaire", bold=True, width="15%"))
    self.header_panel.add_component(Label(text="%", bold=True, width="10%"))
    self.header_panel.add_component(Label(text="Type", bold=True, width="10%"))
    self.header_panel.add_component(Label(text="Groupe", bold=True, width="15%"))
    self.header_panel.add_component(Label(text="Sous-groupe", bold=True, width="15%"))
    self.header_panel.add_component(Label(text="🗑", bold=True, width="5%"))

    # Lignes de test
    self.repeating_participations.items = [
      {
        "societe": "SEB",
        "actionnaire": "Holding ANIS",
        "pourcentage": 51,
        "type": "Personne",
        "groupe": "Agro",
        "sous_groupe": "Pain"
      },
      {
        "societe": "SEM",
        "actionnaire": "Holding ANIS",
        "pourcentage": 49,
        "type": "Personne",
        "groupe": "Meunerie",
        "sous_groupe": "Farine"
      }
    ]
