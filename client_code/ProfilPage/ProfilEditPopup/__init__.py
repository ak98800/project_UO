from ._anvil_designer import ProfilEditPopupTemplate
from anvil import *
import anvil.users
import anvil.server

class ProfilEditPopup(ProfilEditPopupTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

    self.user = anvil.users.get_user()
    self.profil = anvil.server.call("get_profil", self.user)

    if self.profil:
      self.name_box.text = self.profil["name"]
      self.fonction_box.text = self.profil["fonction"]
      self.organisation_box.text = self.profil["organisation"]["name"] if self.profil["organisation"] else ""

      # Organisation modifiable uniquement si admin
      self.organisation_box.enabled = self.profil["is_admin"]

  def save_button_click(self, **event_args):
    try:
      # Mise à jour des champs de profil
      anvil.server.call("update_profil", self.user, self.name_box.text, self.fonction_box.text)

      # Si admin, mise à jour de l'organisation
      if self.profil["is_admin"]:
        anvil.server.call("update_organisation_name", self.profil["organisation"], self.organisation_box.text)

      Notification("Profil mis à jour avec succès.", style="success").show()
      self.raise_event("x-close-alert")

    except Exception as e:
      Notification(f"Erreur : {e}", style="danger").show()
