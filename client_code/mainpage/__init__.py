from ._anvil_designer import mainpageTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class mainpage(mainpageTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.setup_navigation()   # Ajouter la configuration du menu
    self.show_initial_page()  # Afficher LandingPage ou Dashboard au départ

  def setup_navigation(self):
    """Configurer quels boutons sont visibles"""
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

  def show_initial_page(self):
    """Afficher LandingPage ou Dashboard au démarrage"""
    self.content_panel.clear()
    if anvil.users.get_user():
      from ..Dashboard import Dashboard
      self.content_panel.add_component(Dashboard())
    else:
      from ..LandingPage import LandingPage
      self.content_panel.add_component(LandingPage())

  def load_page(self, page_instance):
    """Changer dynamiquement la page affichée"""
    self.content_panel.clear()
    self.content_panel.add_component(page_instance)

  def se_connecter_click(self, **event_args):
    """Clique sur Se connecter"""
    from ..LoginPage import LoginPage
    self.load_page(LoginPage())

  def inscription_click(self, **event_args):
    """Clique sur Inscription"""
    from ..SignUpPage import SignUpPage
    self.load_page(SignUpPage())

  def dashboard_click(self, **event_args):
    """Clique sur Dashboard"""
    from ..Dashboard import Dashboard
    self.load_page(Dashboard())

  def deconnexion_click(self, **event_args):
    """Clique sur Déconnexion"""
    anvil.users.logout()
    self.setup_navigation()
    from ..LandingPage import LandingPage
    self.load_page(LandingPage())
