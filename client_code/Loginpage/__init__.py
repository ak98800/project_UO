from ._anvil_designer import LoginPageTemplate
from anvil import *
import anvil.users

class LoginPage(LoginPageTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

  def login_button_click(self, **event_args):
    """Quand on clique sur 'Se connecter'"""
    email = self.email_textbox.text
    password = self.password_textbox.text

    try:
      anvil.users.login(email, password)
      Notification("Connexion réussie !", style="success").show()
      from ..Dashboard import Dashboard
      get_open_form().load_page(Dashboard())

    except anvil.users.AuthenticationFailed:
      Notification("Email ou mot de passe incorrect.", style="danger").show()
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class Loginpage(LoginpageTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def text_1_show(self, **event_args):
    """This method is called when the component is shown on the screen."""
    pass

  def text_2_show(self, **event_args):
    """This method is called when the component is shown on the screen."""
    pass
