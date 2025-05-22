from ._anvil_designer import WelcomeResetPageTemplate
from anvil import *
import anvil.users
import anvil.server

class WelcomeResetPage(WelcomeResetPageTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

    # ✅ Récupérer l'utilisateur connecté
    self.user = anvil.users.get_user()
    if not self.user:
      Notification("Veuillez vous connecter.", style="danger").show()
      open_form("mainpage")
      return

    # ✅ Afficher l'email
    self.email_label.text = f"Email : {self.user['email']}"

    # ✅ Vérifier si le reset a déjà été envoyé
    if self.user.get("has_reset_password", False):
      self.reset_button.visible = False
      self.message_label.text = "Mot de passe déjà réinitialisé."
    else:
      self.message_label.text = "Cliquez sur le bouton ci-dessous pour définir votre mot de passe."

  def reset_button_click(self, **event_args):
    try:
      if not self.user.get("confirmed_email", False):
        Notification("Veuillez confirmer votre adresse email d'abord.", style="warning").show()
        return
  
      anvil.users.send_password_reset_email(self.user["email"])
      self.reset_button.visible = False
      self.message_label.text = "Un email de réinitialisation vous a été envoyé."
      Notification("Email envoyé avec succès.", style="success").show()
  
    except Exception as e:
      Notification(f"Erreur : {e}", style="danger").show()


