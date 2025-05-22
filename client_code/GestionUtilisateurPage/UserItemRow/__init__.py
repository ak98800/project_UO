from ._anvil_designer import UserItemRowTemplate
from anvil import *

class UserItemRow(UserItemRowTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

    profil = self.item
    user = profil["user"]

    self.name_label.text = profil["name"]
    self.email_label.text = user["email"]
    self.role_label.text = "Admin" if profil["is_admin"] else "Membre"

  def remove_button_click(self, **event_args):
    if confirm(f"Supprimer {self.item['user'].get_email()} de l'organisation ?"):
      try:
        anvil.server.call("supprimer_utilisateur", self.item)
        Notification("Utilisateur supprimé", style="success").show()
        self.raise_event("x-refresh")
      except Exception as e:
        Notification(f"Erreur : {e}", style="danger").show()
