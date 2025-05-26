from ._anvil_designer import SocieteSyntheseRowTemplate
from anvil import *
from ...PageFicheParticipation import PageFicheParticipation

class SocieteSyntheseRow(SocieteSyntheseRowTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

    societe = self.item.get("societe", "")
    nb_actionnaires = self.item.get("nb_actionnaires", 0)
    pourcentage = self.item.get("total_pourcentage", 0)
    statut = self.item.get("statut", "")

    self.societe_label.text = societe
    self.nb_label.text = str(nb_actionnaires)
    self.pourcentage_label.text = f"{pourcentage:.1f} %"
    self.statut_label.text = statut

  def consulter_button_click(self, **event_args):
    
    fiche = PageFicheParticipation(
      dossier=self.item["dossier"],
      nom_societe=self.item["societe"]
    )

    page = self._get_page_dossier()
    if page:
      page.clear_zone_contenu()
      page.zone_contenu.add_component(fiche)

  def _get_page_dossier(self):
    parent = self.parent
    while parent and not hasattr(parent, "zone_contenu"):
      parent = parent.parent
    return parent
