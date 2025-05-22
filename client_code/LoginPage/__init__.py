from ._anvil_designer import LoginPageTemplate
from anvil import *
import anvil.users
import anvil.server

from ..Dashboard import Dashboard  # ← Import de la page principale après login

class LoginPage(LoginPageTemplate):
  def __init__(self, confirmed=False, **properties):
    self.init_components(**properties)

    if confirmed:
      Notification("Votre adresse email a bien été confirmée.", style="success").show()

  def login_button_click(self, **event_args):
    email = self.email_textbox.text
    password = self.password_textbox.text

    try:
      anvil.users.login_with_email(email, password)
      user = anvil.users.get_user()

      if user and user["enabled"]:
        Notification("Connexion réussie !", style="success").show()

        # ✅ Ouvre directement le Dashboard avec la navigation intégrée
        open_form(Dashboard())

      else:
        Notification("Merci de confirmer votre adresse email.", style="warning").show()
        anvil.users.logout()

    except anvil.users.AuthenticationFailed:
      Notification("Email ou mot de passe incorrect.", style="danger").show()


  def reset_password_link_click(self, **event_args):
    email = self.email_textbox.text.strip()
    if not email:
      Notification("Veuillez entrer votre adresse email pour recevoir un lien de réinitialisation.", style="warning").show()
      return

    try:
      anvil.users.send_password_reset_email(email)
      Notification("Un lien de réinitialisation a été envoyé à votre adresse email.", style="success").show()
    except Exception as e:
      Notification(f"Erreur : {e}", style="danger").show()



