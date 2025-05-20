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

    print("✅ HomePageLayout actif")
    self.footer_label.role = "footer"

    # Afficher par défaut le Dashboard
    self.afficher_page(Dashboard(user=self.user))

  def afficher_page(self, composant):
    self.slot_content.clear()
    self.slot_content.add_component(composant)

  def navigation_link_dashboard_click(self, **event_args):
    from ..Dashboard import Dashboard
    self.afficher_page(Dashboard(user=self.user))

  def navigation_link_profil_click(self, **event_args):
    from ..ProfilPage import ProfilPage
    self.afficher_page(ProfilPage())

  def navigation_link_utilisateurs_click(self, **event_args):
    from ..GestionUtilisateursPage import GestionUtilisateursPage
    self.afficher_page(GestionUtilisateursPage())

  def navigation_link_logout_click(self, **event_args):
    anvil.users.logout()
    open_form("mainpage")
