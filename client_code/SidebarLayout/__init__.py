from ._anvil_designer import SidebarLayoutTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class SidebarLayout(SidebarLayoutTemplate):
  def __init__(self, confirmed=False, **properties):
    self.init_components(**properties)
    self.setup_navigation()
    self.show_initial_page(confirmed)

  def setup_navigation(self):
    """Afficher ou masquer les boutons selon l’état de connexion"""
    user = anvil.users.get_user()

    self.se_connecter.visible = False
    self.inscription.visible = False
    self.dashboard.visible = False
    self.deconnexion.visible = False
    self.profil.visible = False

    if user:
      self.dashboard.visible = True
      self.deconnexion.visible = True
      self.profil.visible = True
    else:
      self.se_connecter.visible = True
      self.inscription.visible = True

  def show_initial_page(self, confirmed):
    """Logique de démarrage"""
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
      Notification(
        "Merci de confirmer votre adresse email avant de continuer.", style="warning"
      ).show()
      anvil.users.logout()
      from ..LoginPage import LoginPage

      self.content_panel.add_component(LoginPage())

    else:
      from ..LandingPage import LandingPage

      self.content_panel.add_component(LandingPage())

  def load_page(self, page_instance):
    """Charger une page manuellement"""
    self.content_panel.clear()
    self.content_panel.add_component(page_instance)

  def se_connecter_click(self, **event_args):
    """Clic sur Se connecter"""
    from ..LoginPage import LoginPage

    self.load_page(LoginPage())

  def inscription_click(self, **event_args):
    """Clic sur Inscription"""
    from ..SignUpPage import SignUpPage

    self.load_page(SignUpPage())

  def dashboard_click(self, **event_args):
    """Clic sur Dashboard"""
    from ..Dashboard import Dashboard

    self.load_page(Dashboard())

  def deconnexion_click(self, **event_args):
    """Clic sur Déconnexion"""
    anvil.users.logout()
    self.setup_navigation()
    from ..LandingPage import LandingPage

    self.load_page(LandingPage())

  def profil_click(self, **event_args):
    from ..ProfilPage import ProfilPage

    self.load_page(ProfilPage())
