from ._anvil_designer import mainpage_copyTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import anvil.users

class mainpage_copy(mainpage_copyTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

    user = anvil.users.get_user()
    if user:
      return  # ✅ Laisse HomePageLayout gérer la suite

    self.se_connecter.visible = True
    self.inscription.visible = True

    from ..LandingPage import LandingPage
    self.content_panel.clear()
    self.content_panel.add_component(LandingPage())

  def se_connecter_click(self, **event_args):
    from ..LoginPage import LoginPage
    open_form(LoginPage())

  def inscription_click(self, **event_args):
    from ..SignUpPage import SignUpPage
    open_form(SignUpPage())
