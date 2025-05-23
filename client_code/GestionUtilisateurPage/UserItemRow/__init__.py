from ._anvil_designer import UserItemRowTemplate
from anvil import *
import anvil.server


class UserItemRow(UserItemRowTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

    profil = self.item
    user = profil["user"]

    self.name_label.text = profil["name"]
    self.email_label.text = user["email"]
    self.role_label.text = "Admin" if profil["is_admin"] else "Membre"

  def remove_button_click(self, **event_args):
    if confirm(f"Supprimer {self.item['user']['email']} de l'organisation ?"):
      try:
        anvil.server.call("supprimer_utilisateur", self.item)
        Notification("Utilisateur supprimé", style="success").show()
        self.parent.raise_event("x-refresh")  # ✅ fonctionne comme dans les dossiers
      except Exception as e:
        Notification(f"Erreur : {e}", style="danger").show()



  def form_refreshing_data_bindings(self, **event_args):
    """This method is called when refresh_data_bindings is called"""
    pass



