from ._anvil_designer import LandingPageTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class LandingPage(LandingPageTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

  def se_connecter_button_click(self, **event_args):
    """Quand on clique sur 'Se connecter'"""
    from ..LoginPage import LoginPage
    get_open_form().load_page(LoginPage())

  def commencer_button_click(self, **event_args):
    """Quand on clique sur 'Commencer dès aujourd'hui'"""
    from ..SignUpPage import SignUpPage
    get_open_form().load_page(SignUpPage())

  def creer_compte_button_click(self, **event_args):
    """Quand on clique sur 'Créer mon compte gratuitement'"""
    from ..SignUpPage import SignUpPage
    get_open_form().load_page(SignUpPage())

  def creer_compte_button_show(self, **event_args):
    """This method is called when the component is shown on the screen."""
    pass

  def creer_compte_button_hide(self, **event_args):
    """This method is called when the component is removed from the screen."""
    pass

  def text_1_show(self, **event_args):
    """This method is called when the component is shown on the screen."""
    pass
