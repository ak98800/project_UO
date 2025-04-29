from ._anvil_designer import LoginPageTemplate
from anvil import *
import anvil.users
import anvil.server
import anvil.tables as tables
from anvil.tables import app_tables

class LoginPage(LoginPageTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

  def login_button_click(self, **event_args):
    """Quand on clique sur 'Se connecter'"""
    email = self.email_textbox.text
    password = self.password_textbox.text

    try:
      anvil.users.login(email=email, password=password)
      Notification("Connexion réussie !", style="success").show()

      from ..Dashboard import Dashboard
      get_open_form().load_page(Dashboard())

    except anvil.users.AuthenticationFailed:
      Notification("Email ou mot de passe incorrect.", style="danger").show()
