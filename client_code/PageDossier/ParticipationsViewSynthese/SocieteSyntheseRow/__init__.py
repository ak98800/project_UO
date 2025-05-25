from ._anvil_designer import SocieteSyntheseRowTemplate
from anvil import *

class SocieteSyntheseRow(SocieteSyntheseRowTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    data = self.item

    # Texte principal
    self.societe_label.text = data.get("societe", "?")
    self.nb_label.text = str(data.get("nb_actionnaires", 0))
    self.pct_label.text = f"{round(data.get('total_pourcentage', 0), 2)} %"

    # Couleur selon statut
    statut = data.get("statut", "")
    if statut == "green":
      self.statut_label.text = "✅"
    elif statut == "orange":
      self.statut_label.text = "⚠️"
    elif statut == "red":
      self.statut_label.text = "❌"
    else:
      self.statut_label.text = "❓"

  def voir_fiche_button_click(self, **event_args):
    from ..PageFicheParticipation import PageFicheParticipation
    open_form(PageFicheParticipation(societe=self.item["societe"], dossier=self.item["dossier"]))
