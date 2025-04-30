from ._anvil_designer import mainpageTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class mainpage(mainpageTemplate):
  def __init__(self, confirmed=False, **properties):
    self.init_components(**properties)
    self.setup_navigation()
    self.show_initial_page(confirmed)

  def setup_navigation(self):
    user = anvil.users.get_user()

    self.se_connecter.visible = False
    self.inscription.visible = False
    self.dashboard.visible = False
    self.deconnexion.visible = False

    if user:
      self.dashboard.visible = True
      self.deconnexion.visible = True
    else:
      self.se_connecter.visible = True
      self.inscription.visible = True

  def show_initial_page(self, confirmed):
    self.content_panel.clear()
    user = anvil.users.get_user()

    if user and user["enabled"]:
      if confirmed:
        from ..LoginPage import LoginPage
        self.content_panel.add_component(LoginPage(confirmed=True))
      else:
        from ..Dashboard import Dashboard
        self.content_panel.add_component(Dashboard())

    elif user and not user["enabled"]:
      Notification("Merci de confirmer votre adresse email avant de continuer.", style="warning").show()
      anvil.users.logout()
      from ..LoginPage import LoginPage
      self.content_panel.add_component(LoginPage())

    else:
      from ..LandingPage import LandingPage
      self.content_panel.add_component(LandingPage())

  def load_page(self, page_instance):
    self.content_panel.clear()
    self.content_panel.add_component(page_instance)

  def se_connecter_click(self, **event_args):
    from ..LoginPage import LoginPage
    self.load_page(LoginPage())

  def inscription_click(self, **event_args):
    from ..SignUpPage import SignUpPage
    self.load_page(SignUpPage())

  def dashboard_click(self, **event_args):
    from ..Dashboard import Dashboard
    self.load_page(Dashboard())

  def deconnexion_click(self, **event_args):
    anvil.users.logout()
    self.setup_navigation()
    from ..LandingPage import LandingPage
    self.load_page(LandingPage())
