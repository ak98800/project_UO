from ._anvil_designer import UserRowTemplate
from anvil import *
import anvil.server

class UserRow(UserRowTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

    membre = self.item
    print("✅ Données reçues dans UserRow :", membre)

    self.name_label.text = membre.get("name", "(nom inconnu)")
    self.email_label.text = membre.get("email", "(email inconnu)")
    self.role_label.text = "Admin" if membre.get("is_admin") else "Membre"

    # Lier le clic du bouton supprimer si nécessaire
    self.supprimer_button.set_event_handler("click", self.supprimer_button_click)

  def supprimer_button_click(self, **event_args):
    if self.item["is_admin"]:
      Notification("Impossible de supprimer un administrateur du dossier.", style="warning").show()
      return  # <- le return doit être ici, DANS le bloc if
  
    if confirm(f"Retirer {self.item.get('email')} du dossier ?"):
      try:
        anvil.server.call("retirer_utilisateur_dossier",
                          self.item["folder_id"],
                          self.item["user_id"])
        Notification("Utilisateur retiré", style="success").show()
        self.parent.raise_event("x-reload-utilisateurs")
      except Exception as e:
        Notification(f"Erreur : {e}", style="danger").show()



