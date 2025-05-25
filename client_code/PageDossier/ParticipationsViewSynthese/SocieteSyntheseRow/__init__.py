from ._anvil_designer import SocieteSyntheseRowTemplate
from anvil import *

class SocieteSyntheseRow(SocieteSyntheseRowTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

    # Données de l'élément
    societe = self.item.get("societe", "")
    nb_actionnaires = self.item.get("nb_actionnaires", 0)
    pourcentage = self.item.get("total_pourcentage", 0)
    statut = self.item.get("statut", "")

    self.societe_label.text = societe
    self.nb_label.text = str(nb_actionnaires)
    self.pourcentage_label.text = f"{pourcentage:.1f} %"
    self.statut_label.text = statut

  def consulter_button_click(self, **event_args):
    from ..PageFicheParticipation import PageFicheParticipation
    open_form(PageFicheParticipation(societe=self.item["societe"]))

