from ._anvil_designer import SocieteSyntheseRowTemplate
from anvil import *
from ...PageFicheParticipation import PageFicheParticipation
import anvil.server

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
    open_form(
      PageFicheParticipation(
        dossier=self.item["dossier"],
        nom_societe=self.item["societe"]
      )
    )


  def _get_page_dossier(self):
    parent = self.parent
    while parent and not hasattr(parent, "zone_contenu"):
      parent = parent.parent
    return parent

  def delete_societe_click(self, **event_args):
    nom_societe = self.item["societe"]
    dossier = self.item["dossier"]
  
    if confirm(f"Supprimer la société '{nom_societe}' et toutes ses participations ?"):
      try:
        anvil.server.call("supprimer_societe_du_dossier", dossier["id"], nom_societe)
        Notification(f"Société '{nom_societe}' supprimée.", style="success").show()
  
        # 🔁 Recharge la vue synthèse après suppression
        page = self._get_page_dossier()
        if page and hasattr(page, "participations_button_click"):
          page.participations_button_click()
      except Exception as e:
        Notification(str(e), style="danger").show()
