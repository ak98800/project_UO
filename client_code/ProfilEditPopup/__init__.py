from ._anvil_designer import ProfilEditPopupTemplate
from anvil import *
import anvil.users
import anvil.server

class ProfilEditPopup(ProfilEditPopupTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.user = anvil.users.get_user()
    self.profil = None

    # ✅ Charger les données tout de suite (remplace form_show)
    self.profil = anvil.server.call("get_profil", self.user)

    if self.profil:
      self.name_box.text = self.profil["name"]
      self.fonction_box.text = self.profil["fonction"]

      orga = self.profil["organisation"]
      self.organisation_box.text = orga["name"] if orga else "Aucune"
      self.organisation_box.enabled = self.profil["is_admin"] if orga else False

  def save_button_click(self, **event_args):
    try:
      anvil.server.call("update_profil", self.user, self.name_box.text, self.fonction_box.text)
      if self.profil["is_admin"]:
        anvil.server.call("update_organisation_name", self.profil["organisation"], self.organisation_box.text)

      Notification("Profil mis à jour avec succès.", style="success").show()
      self.raise_event("x-close-alert", value=True)

    except Exception as e:
      Notification(f"Erreur : {e}", style="danger").show()

  def cancel_button_click(self, **event_args):
    self.raise_event("x-close-alert")

  def delete_button_click(self, **event_args):
    if confirm("Êtes-vous sûr de vouloir supprimer votre compte ? Cette action est irréversible.", large=True):
      try:
        anvil.server.call("delete_user")
        Notification("Compte supprimé. À bientôt...", style="success").show()
        anvil.users.logout()
        open_form("mainpage")
      except Exception as e:
        Notification(f"Erreur : {e}", style="danger").show()
