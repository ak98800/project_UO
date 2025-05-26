from ._anvil_designer import ParticipationsViewSyntheseTemplate
from anvil import *
import anvil.server

class ParticipationsViewSynthese(ParticipationsViewSyntheseTemplate):
  def __init__(self, dossier, **properties):
    self.init_components(**properties)
    self.dossier = dossier

    # Chargement des données avec injection du dossier dans chaque ligne
    societes = anvil.server.call("get_synthese_participations", self.dossier["id"])
    for s in societes:
      s["dossier"] = self.dossier
    self.repeating_panel.items = societes

  def ajouter_societe_button_click(self, **event_args):
    """This method is called when the component is clicked."""
    pass












