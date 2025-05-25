from ._anvil_designer import ParticipationsViewSyntheseTemplate
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
