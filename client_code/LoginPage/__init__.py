from ._anvil_designer import LoginPageTemplate
from anvil import *
import anvil.users
import anvil.server

class LoginPage(LoginPageTemplate):
  def __init__(self, confirmed=False, **properties):
    self.init_components(**properties)

    # Si redirigé depuis le lien de confirmation
    if confirmed:
      Notification(
        "Votre adresse email a bien été confirmée. Vous pouvez maintenant vous connecter.",
        style="success"
      ).show()

  def login_button_click(self, **event_args):
    email = self.email_textbox.text
    password = self.password_textbox.text

    try:
      anvil.users.login_with_email(email=email, password=password)

      user = anvil.users.get_user()
      if user and user["enabled"]:
        Notification("Connexion réussie !", style="success").show()
        from ..Dashboard import Dashboard
        get_open_form().load_page(Dashboard())
      else:
        Notification("Merci de confirmer votre adresse email avant de continuer.", style="warning").show()
        anvil.users.logout()

    except anvil.users.AuthenticationFailed:
      Notification("Email ou mot de passe incorrect.", style="danger").show()

  def resend_email_button_click(self, **event_args):
    try:
      anvil.users.send_confirmation_email()
      Notification("Email de confirmation renvoyé avec succès.", style="success").show()
    except Exception as e:
      Notification(f"Erreur : {e}", style="danger").show()
