from ._anvil_designer import archive_GestionUtilisateursPageTemplate
from anvil import *
import anvil.server
import anvil.users

class archive_GestionUtilisateursPage(archive_GestionUtilisateursPageTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.user = anvil.users.get_user()
    self.profil = anvil.server.call("get_profil", self.user)

    if not (self.user and self.profil and self.profil["is_admin"]):
      Notification("Accès réservé aux administrateurs.", style="danger").show()
      return

    self.recharger_utilisateurs()

  def inviter_button_click(self, **event_args):
    email = self.email_textbox.text.strip()
    if not email:
      Notification("Veuillez entrer une adresse email.", style="warning").show()
      return

    try:
      msg = anvil.server.call("inviter_utilisateur", email, self.profil["organisation"])
      Notification(msg, style="success").show()
      self.recharger_utilisateurs()
      self.email_textbox.text = ""
    except Exception as e:
      Notification(f"Erreur : {e}", style="danger").show()

  def recharger_utilisateurs(self):
    users = anvil.server.call("lister_utilisateurs_organisation", self.profil["organisation"])
    self.users_panel.items = users
