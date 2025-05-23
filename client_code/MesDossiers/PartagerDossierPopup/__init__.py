from ._anvil_designer import PartagerDossierPopupTemplate
from anvil import *
import anvil.server

class PartagerDossierPopup(PartagerDossierPopupTemplate):
  def __init__(self, dossier, **properties):
    self.init_components(**properties)
    self.dossier = dossier



    self.nom_dossier_label.text = f"Dossier : {dossier['nom']}"
    self.utilisateur_dropdown.include_placeholder = True
    self.charger_utilisateurs_organisation()

  def charger_utilisateurs_organisation(self):
    try:
      membres = anvil.server.call("lister_utilisateurs_organisation", self.dossier["organisation"])
      utilisateurs_possibles = [
        (f"{m['name']} ({m['user']['email']})", m) for m in membres
        if m["user"] != anvil.users.get_user()
      ]
      self.utilisateur_dropdown.items = utilisateurs_possibles
    except Exception as e:
      Notification(f"Erreur chargement membres : {e}", style="danger").show()

  def partager_button_click(self, **event_args):
    selection = self.utilisateur_dropdown.selected_value
    if not selection:
      Notification("Veuillez choisir un utilisateur.", style="warning").show()
      return

    try:
      msg = anvil.server.call("partager_dossier_avec_utilisateur", selection, self.dossier["id"])
      Notification(msg, style="success").show()

      # ✅ Fermer le popup automatiquement
      self.raise_event("x-close-alert")

      # ✅ Et rafraîchir la liste
      self.raise_event("x-reload-dossiers")

    except Exception as e:
      Notification(f"Erreur : {e}", style="danger").show()

  def fermer_button_click(self, **event_args):
    self.raise_event("x-close-alert")




