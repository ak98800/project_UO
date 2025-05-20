from ._anvil_designer import HomePageLayoutTemplate
from anvil import *
import anvil.users
from ..Dashboard import Dashboard
from ..ProfilPage import ProfilPage
from ..GestionUtilisateursPage import GestionUtilisateursPage

class HomePageLayout(HomePageLayoutTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.user = anvil.users.get_user()

    # Appliquer le rôle au footer
    self.footer_label.role = "footer"

    # Charger Dashboard par défaut
    self.content_panel.clear()
    self.content_panel.add_component(Dashboard(user=self.user))

  def navigation_link_dashboard_click(self, **event_args):
    self.content_panel.clear()
    self.content_panel.add_component(Dashboard(user=self.user))

  def navigation_link_profil_click(self, **event_args):
    self.content_panel.clear()
    self.content_panel.add_component(ProfilPage())

  def navigation_link_utilisateurs_click(self, **event_args):
    self.content_panel.clear()
    self.content_panel.add_component(GestionUtilisateursPage())

