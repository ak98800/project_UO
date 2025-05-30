from ._anvil_designer import Old_HomePageLayoutTemplate
from anvil import *
import anvil.users

# Import directs
from Dashboard import Dashboard
from ProfilPage import ProfilPage
from GestionUtilisateursPage import GestionUtilisateursPage

class Old_HomePageLayout(Old_HomePageLayoutTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.user = anvil.users.get_user()

    print("✅ HomePageLayout actif")

    # Affiche le Dashboard par défaut
    self.content_panel2.clear()
    self.content_panel2.add_component(Dashboard(user=self.user))

  def navigation_link_dashboard_click(self, **event_args):
    self.content_panel2.clear()
    self.content_panel2.add_component(Dashboard(user=self.user))

  def navigation_link_profil_click(self, **event_args):
    self.content_panel2.clear()
    self.content_panel2.add_component(ProfilPage())

  def navigation_link_utilisateurs_click(self, **event_args):
    self.content_panel2.clear()
    self.content_panel2.add_component(GestionUtilisateursPage())

  def navigation_link_logout_click(self, **event_args):
    anvil.users.logout()
    open_form("mainpage")


