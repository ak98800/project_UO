from ._anvil_designer import HomePageLayoutTemplate
from anvil import *
import anvil.users

# ✅ Import directs sans `..`
import Dashboard
import ProfilPage
import GestionUtilisateursPage

class HomePageLayout(HomePageLayoutTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.user = anvil.users.get_user()

    print("✅ HomePageLayout actif")
    self.footer_label.role = "footer"

    # Affiche Dashboard au démarrage
    self.afficher_page(Dashboard.Dashboard(user=self.user))

  def afficher_page(self, page):
    self.slot_content.clear()
    self.slot_content.add_component(page)



  def navigation_link_dashboard_click(self, **event_args):
    self.afficher_page(Dashboard.Dashboard(user=self.user))

  def navigation_link_profil_click(self, **event_args):
    self.afficher_page(ProfilPage.ProfilPage())

  def navigation_link_utilisateurs_click(self, **event_args):
    self.afficher_page(GestionUtilisateursPage.GestionUtilisateursPage())

  def navigation_link_logout_click(self, **event_args):
    anvil.users.logout()
    open_form("mainpage")
