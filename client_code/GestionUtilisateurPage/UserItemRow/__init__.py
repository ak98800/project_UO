from ._anvil_designer import UserItemRowTemplate
from anvil import *

class UserItemRow(UserItemRowTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

    # Chaque item est une row utilisateur
    user = self.item
    self.name_label.text = user["name"]
    self.email_label.text = user["email"]
    self.role_label.text = "Admin" if user.get("is_admin") else "Membre"

  def remove_button_click(self, **event_args):
    if confirm(f"Supprimer {self.item['email']} de l'organisation ?"):
      try:
        anvil.server.call("supprimer_utilisateur", self.item)
        Notification("Utilisateur supprimé", style="success").show()
        self.parent.raise_event("x-refresh")  # pour rafraîchir depuis la page
      except Exception as e:
        Notification(f"Erreur : {e}", style="danger").show()
