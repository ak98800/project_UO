from ._anvil_designer import ParticipationsViewTemplate
from anvil import *
import anvil.users

class ParticipationsView(ParticipationsViewTemplate):
  def __init__(self, dossier, **properties):
    self.init_components(**properties)
    self.dossier = dossier

    # En-têtes manuels
    self.header_panel.clear()
    self.header_panel.add_component(Label(text="Société", bold=True, width="150"))
    self.header_panel.add_component(Label(text="Actionnaire", bold=True, width="150"))
    self.header_panel.add_component(Label(text="%", bold=True, width="50"))
    self.header_panel.add_component(Label(text="Type", bold=True, width="50"))
    self.header_panel.add_component(Label(text="Groupe", bold=True, width="120"))
    self.header_panel.add_component(Label(text="Sous-groupe", bold=True, width="120"))
    self.header_panel.add_component(Label(text="🗑", bold=True, width="120"))

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
