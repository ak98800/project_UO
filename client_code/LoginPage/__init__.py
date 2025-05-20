from ._anvil_designer import LoginPageTemplate
from anvil import *
import anvil.users
import anvil.server

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
        from ..HomePageLayout import HomePageLayout
        open_form(HomePageLayout(content="dashboard"))
      else:
        Notification("Merci de confirmer votre adresse email.", style="warning").show()
        anvil.users.logout()

    except anvil.users.AuthenticationFailed:
      Notification("Email ou mot de passe incorrect.", style="danger").show()
