from ._anvil_designer import HomePageLayoutTemplate
from anvil import *
import anvil.users
from ..Dashboard import Dashboard
from ..ProfilPage import ProfilPage
from ..GestionUtilisateursPage import GestionUtilisateursPage

class HomePageLayout(HomePageLayoutTemplate):
  def __init__(self, content="dashboard", **properties):
    self.init_components(**properties)
    self.user = anvil.users.get_user()

    self.footer_label.role = "footer"
    self.load_content(content)

  def load_content(self, page):
    self.clear_slots("content_slot")
    if page == "dashboard":
      self.add_component(Dashboard(user=self.user), slot="content_slot")
    elif page == "profil":
      self.add_component(ProfilPage(), slot="content_slot")
    elif page == "utilisateurs":
      self.add_component(GestionUtilisateursPage(), slot="content_slot")

  def navigation_link_dashboard_click(self, **event_args):
    self.load_content("dashboard")

  def navigation_link_profil_click(self, **event_args):
    self.load_content("profil")

  def navigation_link_utilisateurs_click(self, **event_args):
    self.load_content("utilisateurs")

  def navigation_link_logout_click(self, **event_args):
    anvil.users.logout()
    open_form("mainpage")
