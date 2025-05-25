from ._anvil_designer import PageFicheParticipationTemplate
from anvil import *
import anvil.server

class PageFicheParticipation(PageFicheParticipationTemplate):
  def __init__(self, dossier, nom_societe, **properties):
    self.init_components(**properties)
    self.dossier = dossier
    self.nom_societe = nom_societe

    # En-tête
    self.nom_societe_label.text = f"Société : {self.nom_societe}"
    self.total_parts_textbox.text = ""  # à remplir plus tard
    self.groupe_textbox.text = ""
    self.sous_groupe_textbox.text = ""

    # Couleur de statut (placeholder)
    self.statut_label.text = "⚠️ Données à compléter"
    self.statut_label.foreground = "orange"

    # Placeholder pour les lignes d’actionnaires
    self.repeating_participations.items = []

  def ajouter_actionnaire_button_click(self, **event_args):
    from .PopupAjouterActionnaire import PopupAjouterActionnaire
    popup = PopupAjouterActionnaire(self.dossier, self.nom_societe)
    popup.set_event_handler("x-actionnaire-ajoute", self.recharger_lignes)
    alert(popup, large=True, buttons=[])

  def recharger_lignes(self, **event_args):
    self.repeating_participations.items = anvil.server.call(
      "get_participations_pour_societe",
      self.dossier["id"],
      self.nom_societe
    )

  def enregistrer_en_tete_button_click(self, **event_args):
    total = self.total_parts_textbox.text.strip()
    groupe = self.groupe_textbox.text.strip() or None
    sous_groupe = self.sous_groupe_textbox.text.strip() or None
    try:
      anvil.server.call(
        "enregistrer_infos_societe",
        self.dossier["id"],
        self.nom_societe,
        total,
        groupe,
        sous_groupe
      )
      Notification("Informations enregistrées.", style="success").show()
    except Exception as e:
      Notification(str(e), style="danger").show()
